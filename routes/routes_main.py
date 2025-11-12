from flask import Blueprint, render_template

routes_main = Blueprint("routes_main", __name__)

@routes_main.route("/")
def index():
    return render_template("index.html")
