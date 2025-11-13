from models.db import db

class Profesores(db.Model):
    __tablename__ = "profesor"
    id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    categoria = db.Column(db.String(100))
    modalidad = db.Column(db.String(50))
    direccion = db.Column(db.String(200))
    precio_por_hora= db.Column(db.Integer)
    user = db.relationship("Users", back_populates="profesor")
