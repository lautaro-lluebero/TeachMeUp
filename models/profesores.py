from models.db import db

class Profesores(db.Model):
    __tablename__ = "profesor"
    id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    categoria = db.Column(db.String(100))
    direccion = db.Column(db.String(200))
    user = db.relationship("Users", back_populates="profesor")
