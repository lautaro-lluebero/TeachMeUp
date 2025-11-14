document.addEventListener("DOMContentLoaded", () => {
    const button = document.getElementById("chatbot-button");
    const windowBox = document.getElementById("chatbot-window");
    const closeBtn = document.getElementById("chatbot-close");
    const sendBtn = document.getElementById("chatbot-send");
    const msgBox = document.getElementById("chatbot-messages");
    const input = document.getElementById("chatbot-input");

    function appendMessage(text, type) {
        const div = document.createElement("div");
        div.classList.add(type === "user" ? "message-user" : "message-bot");
        div.textContent = text;
        msgBox.appendChild(div);
        msgBox.scrollTop = msgBox.scrollHeight;
    }

    async function sendMessage() {
        const text = input.value.trim();
        if (!text) return;

        appendMessage(text, "user");
        input.value = "";

        const res = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: text })
        });

        const data = await res.json();
        appendMessage(data.reply, "bot");
    }

    // --- EVENTOS DE UI ---
    button.addEventListener("click", () => {
        windowBox.style.display = "flex";
    });

    closeBtn.addEventListener("click", () => {
        windowBox.style.display = "none";
    });

    sendBtn.addEventListener("click", sendMessage);
    input.addEventListener("keypress", e => {
        if (e.key === "Enter") sendMessage();
    });

    // --- MENSAJE AUTOMÁTICO PARA ALUMNOS ---
    if (USER_ROLE === "alumno") {
        setTimeout(() => {
            appendMessage(
                `Hola ${USER_NAME}! 👋 Bienvenido a TeachMeUp. ¿Querés que te enseñe a usar la plataforma?`,
                "bot"
            );
        }, 800);
    }
});
