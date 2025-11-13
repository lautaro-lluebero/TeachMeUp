from flask import Flask
from models.db import db

# Importar modelos para que SQLAlchemy conozca todas las clases
from models.users import Users
from models.profesores import Profesores
from models.alumnos import Alumno

# Importar blueprints
from routes.routes_auth import routes_auth
from routes.routes_main import routes_main
from routes.routes_users import routes_users   

from config.config import DATABASE_CONNECTION_URI

app = Flask(__name__)

# Configuración base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_CONNECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "secretkey" 

db.init_app(app)

# Crear base de datos si no existe
with app.app_context():
    db.create_all()

# Registrar Blueprints
app.register_blueprint(routes_auth)
app.register_blueprint(routes_main)
app.register_blueprint(routes_users)   

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
