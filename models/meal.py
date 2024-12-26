from database import db

class Meal(db.Model):
    __tablename__ = "Meals"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    date_time = db.Column(db.DateTime(timezone=True), nullable=False)
    in_diet = db.Column(db.Boolean, nullable=False)