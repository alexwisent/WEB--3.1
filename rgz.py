from flask_login import current_user, login_user, logout_user, login_required
from flask import Blueprint, render_template, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from db.models import users_rgz, medicines

rgz = Blueprint('rgz', __name__)

@rgz.route('/rgz/')
def main():
    if current_user.is_authenticated:
        login = current_user.login
    else:
        login = 'Гость'
    return render_template('rgz/rgz.html', login=login)


@rgz.route('/rgz/register/', methods=['GET', 'POST'])       # Регистрация
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


@rgz.route('/rgz/login/', methods=['GET', 'POST'])      # Вход
def login():
    if request.method == 'GET':
        return render_template('rgz/login.html')

    login_form = request.form.get('login', '').strip()
    password_form = request.form.get('password', '').strip()

    if not login_form:
        return render_template('rgz/login.html', error='Логин не может быть пустым')
    if not password_form:
        return render_template('rgz/login.html', error='Пароль не может быть пустым')

    user = users_rgz.query.filter_by(login=login_form).first()

    if user and check_password_hash(user.password, password_form):
        login_user(user, remember=False)
        return redirect('/rgz/')
    
    return render_template('rgz/login.html', error='Неверный логин или пароль')


@rgz.route('/rgz/logout/')      # Выход
def logout():
    logout_user()
    return redirect('/rgz/')


@rgz.route('/rgz/medicines/')
@login_required
def medicine_list():
    # Получаем параметр страницы, по умолчанию 1
    page = request.args.get('page', 1, type=int)
    per_page = 10  # количество препаратов на странице

    # Запрос к базе с пагинацией
    pagination = medicines.query.order_by(medicines.id).paginate(page=page, per_page=per_page)
    meds = pagination.items

    return render_template('rgz/medicines.html', medicines=meds, pagination=pagination)