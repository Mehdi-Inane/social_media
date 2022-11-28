from datetime import datetime
from config import *
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)
now = datetime.now()

# models
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    posts = db.relationship("Tweet", cascade="all, delete")


class Tweet(db.Model):
    __tablename__ = "tweets"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    body = db.Column(db.String(2048))
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


class Following(db.Model):
    __tablename__ = "follows"
    id_1 = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False,primary_key = True)
    id_2 = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False,primary_key = True)