from models.db import db

class Profesores(db.Model):
    __tablename__ = "profesor"
    id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    nombre_profesor = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    nivel= db.Column(db.String(70), nullable=False)
    descripcion = db.Column(db.Text, nullable=False) 
    modalidad = db.Column(db.String(50), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    celular=db.Column(db.String(200), nullable=False)
    precio_por_hora= db.Column(db.Integer, nullable=False)
    user = db.relationship("Users", back_populates="profesor")
