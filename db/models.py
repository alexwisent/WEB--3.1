from . import db
from flask_login import UserMixin
from datetime import datetime

class users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(162), nullable=False)


class articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(50), nullable=False)
    article_text = db.Column(db.Text, nullable=False)
    is_favorite = db.Column(db.Boolean, default=False)
    is_public = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    users = db.relationship('users', backref='articles')

class gifts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    box_number = db.Column(db.Integer, unique=True, nullable=False)
    message = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    opened_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    pos_x = db.Column(db.Integer, default=0)  # Позиция X на странице
    pos_y = db.Column(db.Integer, default=0)  # Позиция Y на странице
