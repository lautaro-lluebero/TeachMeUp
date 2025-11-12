from flask import Blueprint, render_template, session 

routes_main = Blueprint("routes_main", __name__)

@routes_main.route("/")
def index():
    # Si no está logueado, muestra la página de bienvenida/registro
    if "logged_in" not in session:
        return render_template("index.html") 
    
    # Si está logueado, muestra la página de inicio del usuario
    return render_template("layout.html")
