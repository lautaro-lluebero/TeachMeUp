from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
from models.db import db
from models.users import Users
from decorators import login_required, admin_required, owner_or_admin
import re

routes_users = Blueprint("routes_users", __name__, url_prefix="/users")

# Helpers de validación 
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def is_valid_email(email: str) -> bool:
    return bool(email and EMAIL_RE.match(email))

def not_empty(*vals) -> bool:
    return all(v and str(v).strip() for v in vals)

# Roles válidos
ALLOWED_ROLES = {"administrador", "profesor", "alumno"}

def normalize_role(rol: str) -> str:
    """Normaliza el rol a una de las opciones válidas."""
    if not rol:
        return "alumno"

    r = rol.strip().lower()

    if r in {"admin", "administrator", "administrador"}:
        return "administrador"
    if r in {"prof", "profe", "profesor"}:
        return "profesor"
    if r in {"alumno", "estudiante", "student"}:
        return "alumno"

    return r  

# CONFIGURACIÓN (solo admin) 
@routes_users.route("/configuracion", methods=["GET"])
@login_required
@admin_required
def configuracion():
    """
    Vista de configuración de usuarios (solo administrador).
    Muestra todos los usuarios para poder editarlos/eliminarlos.
    """
    users = Users.query.order_by(Users.id.asc()).all()
    return render_template("users/configuracion.html", users=users)

# PERFIL (usuario logueado)
@routes_users.route("/perfil", methods=["GET", "POST"])
@login_required
def perfil():
    """
    Perfil del usuario logueado: puede editar solo sus propios datos.
    """
    me_id = session.get("user_id")
    if not me_id:
        return redirect(url_for("routes_auth.login"))

    user = Users.query.get(me_id)
    if not user:
        flash("Usuario no encontrado", "error")
        return redirect(url_for("routes_auth.login"))

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        # Validaciones
        if not not_empty(nombre, email):
            return render_template(
                "users/perfil.html",
                user=user,
                error="Nombre y email son obligatorios",
            )

        if not is_valid_email(email):
            return render_template(
                "users/perfil.html",
                user=user,
                error="Email inválido",
            )

        # Email no puede estar usado por otro usuario
        other = Users.query.filter(
            Users.email == email,
            Users.id != user.id,
        ).first()
        if other:
            return render_template(
                "users/perfil.html",
                user=user,
                error="Ese email ya está en uso",
            )

        # Guardar cambios
        user.nombre = nombre
        user.email = email

        # Si se cargó una nueva contraseña se hashea
        if (password or "").strip():
            user.password = generate_password_hash(password)

        db.session.commit()

        # Actualizar datos en la sesión
        session["username"] = user.nombre
        session["rol"] = user.rol

        flash("Perfil actualizado", "success")
        return redirect(url_for("routes_users.perfil"))

    return render_template("users/perfil.html", user=user)

# EDITAR USUARIO (admin o dueño) 
@routes_users.route("/update/<int:id>", methods=["GET"])
@login_required
@owner_or_admin
def edit_user(id):
    user = Users.query.get(id)
    if not user:
        flash("Usuario no encontrado", "error")
        return redirect(url_for("routes_users.configuracion"))
    return render_template("users/edit_user.html", user=user)

@routes_users.route("/update/<int:id>", methods=["POST"])
@login_required
@owner_or_admin
def update_user(id):
    user = Users.query.get(id)
    if not user:
        flash("Usuario no encontrado", "error")
        return redirect(url_for("routes_users.configuracion"))

    nombre = request.form.get("nombre", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    rol_form = normalize_role(request.form.get("rol", user.rol))

    # Validaciones básicas
    if not not_empty(nombre, email):
        return render_template(
            "users/edit_user.html",
            user=user,
            error="Nombre y email son obligatorios",
        )

    if not is_valid_email(email):
        return render_template(
            "users/edit_user.html",
            user=user,
            error="Email inválido",
        )

    # Evitar duplicado de email en otro usuario
    other = Users.query.filter(
        Users.email == email,
        Users.id != id,
    ).first()
    if other:
        return render_template(
            "users/edit_user.html",
            user=user,
            error="Ese email ya está en uso",
        )

    # ¿Es admin el que edita?
    es_admin = (session.get("rol") or "").lower() == "administrador"

    # Solo el admin puede cambiar el rol
    if es_admin:
        if rol_form not in ALLOWED_ROLES:
            return render_template(
                "users/edit_user.html",
                user=user,
                error=f"Rol inválido: {rol_form}",
            )
        user.rol = rol_form

    # Guardar cambios de nombre/email
    user.nombre = nombre
    user.email = email

    # Actualizar password solo si se envía algo (hasheada)
    if (password or "").strip():
        user.password = generate_password_hash(password)

    db.session.commit()

    # Si se edita al usuario logueado, se refresca la sesión
    if session.get("user_id") == user.id:
        session["username"] = user.nombre
        session["rol"] = user.rol

    flash("Usuario actualizado", "success")
    return redirect(
        url_for("routes_users.configuracion" if es_admin else "routes_users.perfil")
    )

# ELIMINAR USUARIO (solo admin) 
@routes_users.route("/delete/<int:id>", methods=["POST"])
@login_required
@admin_required
def delete_user(id):
    user = Users.query.get(id)
    if not user:
        flash("Usuario no encontrado", "error")
        return redirect(url_for("routes_users.configuracion"))

    db.session.delete(user)
    db.session.commit()
    if session.get("user_id") == id:
        session.clear()

    flash("Usuario eliminado", "success")
    return redirect(url_for("routes_users.configuracion"))

# NUEVO USUARIO 
@routes_users.route("/nuevo", methods=["GET", "POST"])
@login_required
@admin_required
def nuevo_usuario():
    """
    Crear un nuevo usuario (solo administrador).
    """
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        rol_form = normalize_role(request.form.get("rol", "alumno"))

        # Validaciones
        if not not_empty(nombre, email, password):
            return render_template(
                "users/nuevo_usuario.html",
                error="Todos los campos son obligatorios",
                nombre=nombre,
                email=email,
                rol=rol_form,
            )

        if not is_valid_email(email):
            return render_template(
                "users/nuevo_usuario.html",
                error="Email inválido",
                nombre=nombre,
                email=email,
                rol=rol_form,
            )

        if rol_form not in ALLOWED_ROLES:
            return render_template(
                "users/nuevo_usuario.html",
                error=f"Rol inválido: {rol_form}",
                nombre=nombre,
                email=email,
                rol=rol_form,
            )

        # Verificar que el email no exista
        existing = Users.query.filter_by(email=email).first()
        if existing:
            return render_template(
                "users/nuevo_usuario.html",
                error="Ese email ya está registrado",
                nombre=nombre,
                email=email,
                rol=rol_form,
            )
        new_user = Users(
            nombre=nombre,
            email=email,
            password=generate_password_hash(password),
            rol=rol_form,
        )

        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return render_template(
                "users/nuevo_usuario.html",
                error="Error al crear el usuario (email duplicado u otro problema)",
                nombre=nombre,
                email=email,
                rol=rol_form,
            )

        flash("Usuario creado correctamente", "success")
        return redirect(url_for("routes_users.configuracion"))

    # GET
    return render_template("users/nuevo_usuario.html")    