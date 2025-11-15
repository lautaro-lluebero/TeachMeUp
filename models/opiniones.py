
from models.db import db

class Opinion(db.Model):
    __tablename__ = 'opiniones'

    id = db.Column(db.Integer, primary_key=True)
    contenido = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship("Users", back_populates="opiniones")
