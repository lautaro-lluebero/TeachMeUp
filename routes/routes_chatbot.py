from flask import Blueprint, request, jsonify, session
import os
import requests
from dotenv import load_dotenv

load_dotenv()

chatbot_bp = Blueprint("chatbot_bp", __name__, url_prefix="/api")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

@chatbot_bp.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "").lower()

    rol = (session.get("rol") or "").lower()
    nombre = session.get("username") or "usuario"

    # ---------------------------
    # PALABRAS CLAVE PERSONALIZADAS
    # ---------------------------

    # HOLA
    if user_msg in ["hola", "holaa", "buenas"]:
        return jsonify({"reply": f"¡Hola {nombre}! 😊 ¿Te ayudo a usar TeachMeUp?"})

    # SI → iniciar tutorial
    if user_msg in ["si", "sí", "dale", "ok"]:
        if rol == "alumno":
            tutorial = (
                f"¡Perfecto {nombre}! Te enseño cómo usar TeachMeUp:\n\n"
                "1️⃣ Perfil: arriba a la derecha podés ver tus datos.\n"
                "2️⃣ Profesores: buscá docentes desde la barra superior.\n"
                "3️⃣ Inicio: el logo te devuelve al inicio.\n"
                "4️⃣ Configuración: en tu perfil cambiás todo.\n"
                "5️⃣ Chatbot: podés preguntarme dudas cuando quieras.\n\n"
                "¿Querés que te muestre cómo buscar profesores?"
            )
            return jsonify({"reply": tutorial})
        else:
            return jsonify({"reply": "¡Perfecto! ¿Qué querés hacer?"})

    # NO → cancelar
    if user_msg in ["no", "no gracias"]:
        return jsonify({"reply": "¡Listo! Si necesitás algo, acá estoy 👍"})

    # ---------------------------
    # SI NO ES PALABRA CLAVE → IA GROQ
    # ---------------------------

    contexto_general = (
        "Sos TeachMeUp AI, el asistente educativo que ayuda y guía a los usuarios."
    )

    if rol == "alumno":
        contexto_rol = f"El usuario es un alumno llamado {nombre}. Explicale TeachMeUp."
    elif rol == "profesor":
        contexto_rol = f"El usuario es profesor llamado {nombre}."
    else:
        contexto_rol = f"El usuario se llama {nombre}."

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    body = {
        "model": "llama3-8b-262k",
        "messages": [
            {"role": "system", "content": contexto_general + " " + contexto_rol},
            {"role": "user", "content": user_msg}
        ]
    }

    resp = requests.post(GROQ_URL, json=body, headers=headers)
    data = resp.json()

    if "choices" not in data:
        return jsonify({"reply": f"Error Groq: {data}"})

    return jsonify({"reply": data["choices"][0]["message"]["content"]})
