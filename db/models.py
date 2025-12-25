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

class users_rgz(db.Model, UserMixin):
    __tablename__ = 'users_rgz'     # явное указание имени на всякий случай

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(162), nullable=False)

class medicines(db.Model):
    __tablename__ = 'medicines'     # явное указание имени на всякий случай 

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)              # торговое название
    international_name = db.Column(db.String(100), nullable=False)  # МНН
    prescription_only = db.Column(db.Boolean, nullable=False)     # только по рецепту
    price = db.Column(db.Numeric(10, 2), nullable=False)          # цена
    quantity = db.Column(db.Integer, nullable=False)              # количество
