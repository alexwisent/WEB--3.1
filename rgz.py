from flask_login import current_user, login_user, logout_user, login_required
from flask import Blueprint, render_template, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from db.models import users, medicines
from sqlalchemy import or_, and_

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
    if request.method == 'GET':     # Отображение формы регистрации
        return render_template('rgz/register.html')

    login_form = request.form.get('login', '').strip()      # Получаем логин из формы
    password_form = request.form.get('password', '').strip()    # Получаем пароль из формы

    # Валидация
    if not login_form:
        return render_template('rgz/register.html', error='Логин не может быть пустым')
    if not password_form:
        return render_template('rgz/register.html', error='Пароль не может быть пустым')
    
    # Проверка на уникальность
    if users.query.filter_by(login=login_form).first():
        return render_template('rgz/register.html', error='Пользователь с таким логином уже существует')

    # Хеширование пароля
    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)

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

    user = users.query.filter_by(login=login_form).first()  # Ищем пользователя в БД

    if user and check_password_hash(user.password, password_form):  # Проверяем пароль
        login_user(user, remember=False)    # Авторизуем пользователя
        return redirect('/rgz/')
    
    return render_template('rgz/login.html', error='Неверный логин или пароль')


@rgz.route('/rgz/logout/')  # Выход
def logout():   # Выход пользователя
    logout_user()   # Завершаем сессию
    return redirect('/rgz/')


@rgz.route('/rgz/medicines/')   # Список препаратов
def medicine_list():
    # Получаем параметры поиска из query string
    search_name = request.args.get('name', '').strip()
    max_price = request.args.get('price', '').strip()
    prescription_only = request.args.get('prescription_only')

    page = request.args.get('page', 1, type=int)    # Текущая страница
    per_page = 10

    query = medicines.query

    if search_name: # Фильтр по названию
        query = query.filter(medicines.name.ilike(f'%{search_name}%'))
    
    if max_price:   # Фильтр по цене
        try:
            max_price_val = float(max_price)
            query = query.filter(medicines.price <= max_price_val)
        except ValueError:
            pass  # если введено не число, игнорируем

    if prescription_only == 'on':
        query = query.filter(medicines.prescription_only == True)   # Только рецептурные

    pagination = query.order_by(medicines.id).paginate(page=page, per_page=per_page)    # Пагинация
    meds = pagination.items # Текущая страница препаратов

    return render_template('rgz/medicines.html', medicines=meds, pagination=pagination, search_name=search_name, max_price=max_price, prescription_only=prescription_only)



@rgz.route('/rgz/add_medicine/', methods=['GET', 'POST'])   # Добавление препаратов
@login_required
def add_medicine():
    # Разрешено только администратору
    if current_user.login != 'admin':
        return "У вас нет прав для добавления препаратов", 403

    if request.method == 'GET':
        return render_template('rgz/add_medicine.html')

    # Получаем данные из формы
    name = request.form.get('name', '').strip()
    international_name = request.form.get('international_name', '').strip()
    prescription_only = request.form.get('prescription_only') == 'on'
    price = request.form.get('price', '').strip()
    quantity = request.form.get('quantity', '').strip()

    # Валидация
    if not name or not international_name or not price or not quantity:
        return render_template('rgz/add_medicine.html', error='Все поля обязательны')

    try:
        price = float(price)
        quantity = int(quantity)
    except ValueError:
        return render_template('rgz/add_medicine.html', error='Цена и количество должны быть числами')

    if price <= 0:
        return render_template('rgz/add_medicine.html', error='Цена должна быть больше 0')
    if quantity < 0:
        return render_template('rgz/add_medicine.html', error='Количество не может быть отрицательным')

    # Создаём новый препарат
    new_med = medicines(
        name=name,
        international_name=international_name,
        prescription_only=prescription_only,
        price=price,
        quantity=quantity
    )

    db.session.add(new_med)
    db.session.commit()

    return redirect('/rgz/medicines/')


@rgz.route('/rgz/edit_medicine/<int:med_id>/', methods=['GET', 'POST'])     # Редактирование препаратов
@login_required
def edit_medicine(med_id):
    # Только администратор
    if current_user.login != 'admin':
        return "У вас нет прав для редактирования препаратов", 403

    # Получаем препарат по id
    med = medicines.query.get_or_404(med_id)

    if request.method == 'GET':
        # Отправляем текущие данные в форму
        return render_template('rgz/edit_medicine.html', med=med)

    # Получаем данные из формы
    name = request.form.get('name', '').strip()
    international_name = request.form.get('international_name', '').strip()
    prescription_only = request.form.get('prescription_only') == 'on'
    price = request.form.get('price', '').strip()
    quantity = request.form.get('quantity', '').strip()

    # Валидация
    if not name or not international_name or not price or not quantity:
        return render_template('rgz/edit_medicine.html', med=med, error='Все поля обязательны')

    try:
        price = float(price)
        quantity = int(quantity)
    except ValueError:
        return render_template('rgz/edit_medicine.html', med=med, error='Цена и количество должны быть числами')

    if price <= 0:
        return render_template('rgz/edit_medicine.html', med=med, error='Цена должна быть больше 0')
    if quantity < 0:
        return render_template('rgz/edit_medicine.html', med=med, error='Количество не может быть отрицательным')

    # Обновляем данные
    med.name = name
    med.international_name = international_name
    med.prescription_only = prescription_only
    med.price = price
    med.quantity = quantity

    db.session.commit()

    return redirect('/rgz/medicines/')


@rgz.route('/rgz/delete_account/', methods=['GET', 'POST'])
@login_required
def delete_account():
    if request.method == 'GET':
        # Показываем страницу подтверждения удаления
        return render_template('rgz/delete_account.html')

    # POST — подтверждение удаления
    user = current_user

    # Удаляем пользователя из базы
    db.session.delete(user)
    db.session.commit()

    # Выход из системы
    logout_user()

    return redirect('/rgz/')


@rgz.route('/rgz/delete_medicine/<int:med_id>/', methods=['POST'])
@login_required
def delete_medicine(med_id):
    # Только администратор
    if current_user.login != 'admin':
        return "У вас нет прав для удаления препаратов", 403

    med = medicines.query.get_or_404(med_id)

    db.session.delete(med)
    db.session.commit()

    return redirect('/rgz/medicines/')
