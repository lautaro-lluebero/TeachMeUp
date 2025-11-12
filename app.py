from flask import Flask
from dotenv import load_dotenv
from models.db import db
from routes.routes_auth import routes_auth
from routes.routes_main import routes_main

import os
from config.config import DATABASE_CONNECTION_URI
# -----------------------------
# Cargar configuración desde .env
# -----------------------------
load_dotenv()

app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secretkey'
db.init_app(app)

# Create database tables
with app.app_context():
    #db.drop_all()
    db.create_all()

# Registrar Blueprints
app.register_blueprint(routes_auth)
app.register_blueprint(routes_main)


# Crear base de datos si no existe
with app.app_context():
    db.create_all()

# -----------------------------
# Inicio del servidor
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
