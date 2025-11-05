from flask import Blueprint, url_for, redirect, render_template, abort, request, make_response, redirect
import json
import os
lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name', 'аноним')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age', 'неизвестно')
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)     #name=name передача имени в шаблон

@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp

@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp

@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    age = request.args.get('age')
    sex = request.args.get('sex')

    if not user:
        errors['user'] = 'Заполните поле!'

    if not age:
        errors['age'] = 'Заполните поле!'
    
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)

@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')

@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    # Пусть кофе стоит 120 рублей, чёрный чай — 80 рублей, зелёный — 70 рублей. 
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    # Добавка молока удорожает напиток на 30 рублей, а сахара - на 10.
    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/pay.html', price=price)

@lab3.route('/lab3/success')
def success():
    price = request.args.get('price', 0)
    name = request.args.get('name', '')
    
    return render_template('lab3/success.html', price=price, name=name)

@lab3.route('/lab3/settings') #обработчик, который будет принимать цвет и записывать его в куки. 
def settings():
    color = request.args.get('color')
    bgcolor = request.args.get('bgcolor')
    fontsize = request.args.get('fontsize')
    fontstyle = request.args.get('fontstyle')

    if any([color, bgcolor, fontsize, fontstyle is not None]):
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if bgcolor:
            resp.set_cookie('bgcolor', bgcolor)
        if fontsize:
            resp.set_cookie('fontsize', fontsize)
        if fontstyle == '':
            resp.delete_cookie('fontstyle')  # удаляем cookie, если выбрано "Обычный"
        else:
            resp.set_cookie('fontstyle', fontstyle)
        return resp

    color = request.cookies.get('color')
    bgcolor = request.cookies.get('bgcolor')
    fontsize = request.cookies.get('fontsize')
    fontstyle = request.cookies.get('fontstyle')

    resp = make_response(render_template('lab3/settings.html', color=color, bgcolor=bgcolor, fontsize=fontsize, fontstyle=fontstyle))
    return resp

@lab3.route('/lab3/train_ticket', methods=['GET', 'POST'])
def train_ticket():
    errors = {}
    ticket_data = {}
    price = 0

    if request.method == 'POST':
        # Получаем данные формы
        fio = request.form.get('fio', '').strip()
        berth = request.form.get('berth', '')
        bedding = request.form.get('bedding')
        luggage = request.form.get('luggage')
        age = request.form.get('age', '').strip()
        departure = request.form.get('departure', '').strip()
        destination = request.form.get('destination', '').strip()
        travel_date = request.form.get('travel_date', '').strip()
        insurance = request.form.get('insurance')

        # Проверка всех обязательных полей
        if not fio:
            errors['fio'] = 'Введите ФИО!'
        if not berth:
            errors['berth'] = 'Выберите полку!'
        if not age:
            errors['age'] = 'Введите возраст!'
        else:
            try:
                age = int(age)
                if age < 1 or age > 120:
                    errors['age'] = 'Возраст должен быть от 1 до 120!'
            except ValueError:
                errors['age'] = 'Возраст должен быть числом!'
        if not departure:
            errors['departure'] = 'Введите пункт выезда!'
        if not destination:
            errors['destination'] = 'Введите пункт назначения!'
        if not travel_date:
            errors['travel_date'] = 'Введите дату поездки!'

        # Если ошибок нет — считаем цену
        if not errors:
            # Базовая цена
            if age < 18:
                price = 700
                ticket_type = "Детский билет"
            else:
                price = 1000
                ticket_type = "Взрослый билет"

            # Доплаты
            if berth in ['нижняя', 'нижняя боковая']:
                price += 100
            if bedding == 'on':
                price += 75
            if luggage == 'on':
                price += 250
            if insurance == 'on':
                price += 150

            # Формируем данные билета
            ticket_data = {
                'fio': fio,
                'berth': berth,
                'bedding': bedding,
                'luggage': luggage,
                'age': age,
                'departure': departure,
                'destination': destination,
                'travel_date': travel_date,
                'insurance': insurance,
                'price': price,
                'ticket_type': ticket_type
            }

            return render_template('lab3/train_ticket_result.html', ticket=ticket_data)

    # Если GET или есть ошибки
    return render_template('lab3/train_ticket_form.html', errors=errors, request=request)

@lab3.route('/lab3/settings/clear')
def clear_settings():
    response = make_response(redirect(url_for('lab3.settings')))    # Создаем ответ с редиректом
    cookies_to_clear = ['color', 'bgcolor', 'fontsize', 'fontstyle']    # Очищаем все куки, связанные с настройками
    
    for cookie_name in cookies_to_clear:
        response.set_cookie(cookie_name, '', max_age=0)
    return response


@lab3.route('/lab3/products', methods=['GET'])
def products():
    # --- список товаров ---
    products = [
        {'name': 'iPhone 15', 'price': 120000, 'brand': 'Apple', 'color': 'черный'},
        {'name': 'Samsung Galaxy S24', 'price': 95000, 'brand': 'Samsung', 'color': 'серый'},
        {'name': 'Xiaomi 14', 'price': 60000, 'brand': 'Xiaomi', 'color': 'синий'},
        {'name': 'Google Pixel 8', 'price': 88000, 'brand': 'Google', 'color': 'черный'},
        {'name': 'Huawei P60', 'price': 77000, 'brand': 'Huawei', 'color': 'белый'},
        {'name': 'Realme GT 5', 'price': 50000, 'brand': 'Realme', 'color': 'серый'},
        {'name': 'OnePlus 12', 'price': 85000, 'brand': 'OnePlus', 'color': 'зеленый'},
        {'name': 'Sony Xperia 1 V', 'price': 110000, 'brand': 'Sony', 'color': 'черный'},
        {'name': 'Honor Magic6', 'price': 68000, 'brand': 'Honor', 'color': 'бежевый'},
        {'name': 'Asus ROG Phone 8', 'price': 115000, 'brand': 'Asus', 'color': 'черный'},
        {'name': 'Nokia X30', 'price': 43000, 'brand': 'Nokia', 'color': 'синий'},
        {'name': 'ZTE Axon 50', 'price': 47000, 'brand': 'ZTE', 'color': 'серый'},
        {'name': 'Vivo X100', 'price': 72000, 'brand': 'Vivo', 'color': 'черный'},
        {'name': 'Infinix Zero 30', 'price': 35000, 'brand': 'Infinix', 'color': 'золотой'},
        {'name': 'Tecno Phantom X2', 'price': 40000, 'brand': 'Tecno', 'color': 'серый'},
        {'name': 'Motorola Edge 40', 'price': 56000, 'brand': 'Motorola', 'color': 'красный'},
        {'name': 'Apple iPhone SE', 'price': 60000, 'brand': 'Apple', 'color': 'белый'},
        {'name': 'Samsung A55', 'price': 47000, 'brand': 'Samsung', 'color': 'синий'},
        {'name': 'Xiaomi Redmi Note 13', 'price': 30000, 'brand': 'Xiaomi', 'color': 'черный'},
        {'name': 'Realme C67', 'price': 25000, 'brand': 'Realme', 'color': 'зеленый'}
    ]

    # --- минимальная и максимальная цены ---
    min_price_all = min(p['price'] for p in products)
    max_price_all = max(p['price'] for p in products)

    # --- получаем значения из формы или из куки ---
    min_price = request.args.get('min_price') or request.cookies.get('min_price')
    max_price = request.args.get('max_price') or request.cookies.get('max_price')

    filtered = products

    # Проверяем, нажата ли кнопка сброса
    if request.args.get('reset'):
        resp = make_response(redirect('/lab3/products'))
        resp.delete_cookie('min_price')
        resp.delete_cookie('max_price')
        return resp

    # Преобразуем строки в числа (если заданы)
    try:
        if min_price:
            min_price = int(min_price)
        if max_price:
            max_price = int(max_price)
    except ValueError:
        min_price = None
        max_price = None

    # Если пользователь перепутал местами — меняем
    if min_price and max_price and min_price > max_price:
        min_price, max_price = max_price, min_price

    # Фильтрация по диапазону
    if min_price:
        filtered = [p for p in filtered if p['price'] >= min_price]
    if max_price:
        filtered = [p for p in filtered if p['price'] <= max_price]

    count = len(filtered)

    # Подготавливаем ответ с установкой куки (если заданы)
    resp = make_response(render_template(
        'lab3/products.html',
        products=filtered,
        count=count,
        min_price=min_price,
        max_price=max_price,
        min_price_all=min_price_all,
        max_price_all=max_price_all
    ))

    if min_price:
        resp.set_cookie('min_price', str(min_price))
    if max_price:
        resp.set_cookie('max_price', str(max_price))

    return resp