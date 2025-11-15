from flask import Flask, render_template
from models.db import db

# Importar modelos para que SQLAlchemy conozca todas las clases
from models.users import Users
from models.profesores import Profesores
from models.alumnos import Alumno
from models.opiniones import Opinion

# Importar blueprints existentes
from routes.routes_auth import routes_auth
from routes.routes_main import routes_main
from routes.routes_users import routes_users
from routes.routes_profesores import routes_profesores
from routes.routes_opiniones import routes_opiniones

# Importar blueprint del chatbot
from routes.routes_chatbot import chatbot_bp

from config.config import DATABASE_CONNECTION_URI

app = Flask(__name__)

# Configuración base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_CONNECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "secretkey"

db.init_app(app)

# Crear base de datos si no existe
with app.app_context():
    #db.drop_all()
    db.create_all()

# Registrar Blueprints existentes
app.register_blueprint(routes_auth)
app.register_blueprint(routes_main)
app.register_blueprint(routes_users)
app.register_blueprint(routes_profesores)
app.register_blueprint(routes_opiniones)

# Registrar Blueprint del chatbot
app.register_blueprint(chatbot_bp)

# Ruta para abrir chatbot.html
@app.route("/chatbot")
def mostrar_chatbot():
    return render_template("chatbot.html")

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
