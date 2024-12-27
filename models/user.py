from database import db
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class User(db.Model, UserMixin):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(10), nullable=False, unique=True)
    password = db.Column(db.String(10), nullable=False)
    meals = db.relationship('Meal', backref='user', lazy=True)