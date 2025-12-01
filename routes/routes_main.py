from flask import Blueprint, render_template, session

routes_main = Blueprint("routes_main", __name__)

@routes_main.route("/")
def index():
    if "logged_in" not in session:
        return render_template("index.html") 
    return render_template("principal.html")


@routes_main.route("/profesores")
def profesores():
    return render_template(url_for("routes_profesores.listar_profesores"))
