from flask import Blueprint, url_for, redirect, render_template, abort, request, make_response, redirect
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