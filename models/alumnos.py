from models.db import db

class Alumno(db.Model):
    __tablename__ = "alumno"
    id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    carrera = db.Column(db.String(100), nullable=False)
    nivel = db.Column(db.String(100), nullable=False)
    user = db.relationship("Users", back_populates="alumno")
