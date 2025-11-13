from models.db import db

class Alumno(db.Model):
    __tablename__ = "alumno"
    id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    carrera = db.Column(db.String(100))
    user = db.relationship("Users", back_populates="alumno")
