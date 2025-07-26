from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    roll = db.Column(db.String(20), unique=True)
    math = db.Column(db.Integer)
    science = db.Column(db.Integer)
    english = db.Column(db.Integer)
    total = db.Column(db.Integer)
    percentage = db.Column(db.Float)
