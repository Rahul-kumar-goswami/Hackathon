
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(100), unique=True, nullable=False)
#     password = db.Column(db.String(100), nullable=False)
#     role = db.Column(db.String(20), nullable=False)  # student ya teacher
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(20), nullable=False)

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(120), nullable=False)
    notes = db.Column(db.Text)
    filename = db.Column(db.String(120), nullable=False)
    uploaded_by = db.Column(db.String(80), nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

