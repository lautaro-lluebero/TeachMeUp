from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.db import db
from models.users import Users

routes_auth = Blueprint("routes_auth", __name__, url_prefix="/auth")

# -------------------- Registro --------------------
@routes_auth.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        password = request.form["password"]
        repassword = request.form["repassword"]
        rol = request.form["rol"]

        # Validar contraseñas
        if password != repassword:
            flash("Las contraseñas no coinciden", "error")
            return redirect(url_for("routes_auth.registro"))

        # Verificar si ya existe el correo
        existente = Users.query.filter_by(email=email).first()
        if existente:
            flash("El correo ya está registrado", "warning")
            return redirect(url_for("routes_auth.registro"))

        # Crear usuario nuevo
        hashed_pw = generate_password_hash(password)
        nuevo = Users(nombre=nombre, email=email, password=hashed_pw, rol=rol)

        db.session.add(nuevo)
        db.session.commit()

        flash("Usuario registrado correctamente", "success")
        return redirect(url_for("routes_auth.login"))

    return render_template("registro.html")

# -------------------- Login --------------------
@routes_auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        password = request.form["password"]

        # Buscar usuario por email
        user = Users.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            # Guardar datos en sesión
            session["logged_in"] = True
            session["user_id"] = user.id
            session["username"] = user.nombre
            session["rol"] = user.rol

            flash(f"Bienvenido, {user.nombre} ({user.rol})", "success")
            return render_template("layout.html")
        else:
            flash("Correo o contraseña incorrectos", "error")
            return redirect(url_for("routes_auth.login"))

    return render_template("login.html")

# -------------------- Logout --------------------
@routes_auth.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada correctamente", "info")
    return redirect(url_for("routes_main.index"))
