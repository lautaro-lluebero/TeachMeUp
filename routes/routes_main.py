from flask import Blueprint, render_template, session, redirect, url_for

routes_main = Blueprint("routes_main", __name__)

@routes_main.route("/")
def index():
    if "logged_in" not in session:
        return render_template("index.html") 
    return render_template("principal.html")


@routes_main.route("/profesores")
def profesores():
    # acá vas a cargar a futuro profesores reales desde la DB
    return render_template(url_for("routes_profesores.listar_profesores"))
