from flask import Blueprint, render_template, request, redirect, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from db.models import users, articles

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
    login = session.get('login', 'Anonymous')
    return render_template('lab8/lab8.html', login=login)


@lab8.route('/lab8/login')
def login():
    return "Страница входа (будет реализована позже)"


@lab8.route('/lab8/register')
def register():
    return "Страница регистрации (будет реализована позже)"


@lab8.route('/lab8/articles')
def articles():
    return "Список статей (будет реализован позже)"


@lab8.route('/lab8/create')
def create():
    return "Создание статьи (будет реализовано позже)"




