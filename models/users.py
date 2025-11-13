from models.db import db

class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(50), nullable=False)

    profesor = db.relationship("Profesores", back_populates="user", uselist=False)
    alumno = db.relationship("Alumno", back_populates="user", uselist=False)

    def __init__(self,nombre,email, password, rol):
        self.nombre = nombre
        self.email = email
        self.password= password
        self.rol=rol

    def __repr__(self):
        return f"<User {self.nombre} ({self.rol})>"
