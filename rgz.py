from flask_login import current_user, login_user
from flask import Blueprint, render_template, request, redirect
from werkzeug.security import generate_password_hash
from db import db
from db.models import users_rgz

rgz = Blueprint('rgz', __name__)

@rgz.route('/rgz/')
def main():
    if current_user.is_authenticated:
        login = current_user.login
    else:
        login = 'Гость'
    return render_template('rgz/rgz.html', login=login)


@rgz.route('/rgz/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('rgz/register.html')

    login_form = request.form.get('login', '').strip()
    password_form = request.form.get('password', '').strip()

    # Валидация
    if not login_form:
        return render_template('rgz/register.html', error='Логин не может быть пустым')
    if not password_form:
        return render_template('rgz/register.html', error='Пароль не может быть пустым')
    
    # Проверка на уникальность
    if users_rgz.query.filter_by(login=login_form).first():
        return render_template('rgz/register.html', error='Пользователь с таким логином уже существует')

    # Хеширование пароля
    password_hash = generate_password_hash(password_form)
    new_user = users_rgz(login=login_form, password=password_hash)

    db.session.add(new_user)
    db.session.commit()

    # Автоматический вход после регистрации
    login_user(new_user, remember=False)

    # Редирект на главную страницу
    return redirect('/rgz/')


