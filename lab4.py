from flask import Blueprint, render_template, request, redirect, session
lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')


@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быль заполнены')
    x1 = int(x1)
    x2 = int(x2)
    if x2 == 0:
        return render_template('lab4/div.html', error='Нельзя делитьна 0 /-^-"/')
    else:
        result = x1 / x2
        return render_template('lab4/div.html', x1=x1, x2=x2, result=result)
    

@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')


@lab4.route('/lab4/sum', methods=['POST'])
def sum():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    x1 = int(x1) if x1 else 0
    x2 = int(x2) if x2 else 0
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/mul-form')
def mul_form():
    return render_template('lab4/mul-form.html')


@lab4.route('/lab4/mul', methods=['POST'])
def mul():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    x1 = int(x1) if x1 else 1
    x2 = int(x2) if x2 else 1
    result = x1 * x2
    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')


@lab4.route('/lab4/sub', methods=['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены')
    x1 = int(x1)
    x2 = int(x2)
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('lab4/pow-form.html')


@lab4.route('/lab4/pow', methods=['POST'])
def pow():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены')
    x1 = int(x1)
    x2 = int(x2)
    if x1 == 0 and x2 == 0:
        return render_template('lab4/pow.html', error='0^0 не определено')
    result = x1 ** x2
    return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)


tree_count = 0
max_tree = 10

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'POST':
        operation = request.form.get('operation')

        if operation == 'cut' and tree_count > 0:
            tree_count -= 1
        elif operation == 'plant' and tree_count < max_tree:
            tree_count += 1

        return redirect('/lab4/tree')

    return render_template('lab4/tree.html', tree_count=tree_count, max_tree=max_tree)


users = [
    {'login': 'alex', 'password': '123', 'name': 'Алексей Иванов', 'gender': 'm'},
    {'login': 'bob', 'password': '555', 'name': 'Борис Смирнов', 'gender': 'm'},
    {'login': 'maria', 'password': '789', 'name': 'Мария Сергеева', 'gender': 'f'},
    {'login': 'john', 'password': '000', 'name': 'Джон Смит', 'gender': 'm'},
]


@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login = session.get('name', session['login'])  # берём имя, иначе логин
        else:
            authorized = False
            login = ''
        return render_template("lab4/login.html", authorized=authorized, login=login)

    login_input = request.form.get('login')
    password_input = request.form.get('password')

    # проверка на пустые поля
    if not login_input:
        return render_template('lab4/login.html', error='Не введён логин', authorized=False, login=login_input)
    if not password_input:
        return render_template('lab4/login.html', error='Не введён пароль', authorized=False, login=login_input)

    # поиск пользователя
    for user in users:
        if login_input == user['login'] and password_input == user['password']:
            session['login'] = user['login']
            session['name'] = user['name']   # сохраняем имя
            return redirect('/lab4/login')

    # неверные данные — логин сохраняем
    error = 'Неверные логин и/или пароль'
    return render_template('lab4/login.html', error=error, authorized=False, login=login_input)


@lab4.route('/lab4/logout', methods = ['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')


@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    temperature = request.form.get('temperature')
    if request.method == 'POST':
        # не введено вообще
        if temperature is None or temperature == '':
            return render_template('lab4/fridge.html',
                                   error='Ошибка: не задана температура')

        try:
            temp = int(temperature)
        except ValueError:
            return render_template('lab4/fridge.html',
                                   error='Температура должна быть числом')

        # слишком низко
        if temp < -12:
            return render_template('lab4/fridge.html',
                                   error='Не удалось установить температуру — слишком низкое значение')

        # слишком высоко
        if temp > -1:
            return render_template('lab4/fridge.html',
                                   error='Не удалось установить температуру — слишком высокое значение')

        # диапазоны
        if -12 <= temp <= -9:
            snowflakes = 3
        elif -8 <= temp <= -5:
            snowflakes = 2
        elif -4 <= temp <= -1:
            snowflakes = 1

        return render_template('lab4/fridge.html',
                               temp=temp, snowflakes=snowflakes)

    return render_template('lab4/fridge.html')


@lab4.route('/lab4/grain', methods=['GET', 'POST'])
def grain():
    prices = {
        'ячмень': 12000,
        'овёс': 8500,
        'пшеница': 9000,
        'рожь': 15000
    }

    if request.method == 'POST':
        grain_type = request.form.get('grain_type')
        weight = request.form.get('weight', '').strip()

        # Проверка веса
        if weight == '':
            return render_template('lab4/grain.html', error="Ошибка: не указан вес", grain_type=grain_type)

        try:
            weight = float(weight)
        except ValueError:
            return render_template('lab4/grain.html', error="Вес должен быть числом", grain_type=grain_type)

        if weight <= 0:
            return render_template('lab4/grain.html', error="Ошибка: вес должен быть больше 0", grain_type=grain_type)

        if weight > 100:
            return render_template('lab4/grain.html',
                                   error="Такого объёма сейчас нет в наличии")

        # Расчёт стоимости
        base_price = prices[grain_type]
        total = base_price * weight
        discount_text = ""
        discount_amount = 0

        if weight > 10:
            discount_amount = total * 0.10
            total = total * 0.90
            discount_text = f"Применена скидка 10% — {discount_amount:.2f} руб."

        return render_template(
            'lab4/grain.html',
            grain_type=grain_type,
            weight=weight,
            total=total,
            discount_text=discount_text,
            base_price=base_price
        )

    return render_template('lab4/grain.html')
