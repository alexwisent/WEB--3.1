from flask import Blueprint, url_for, redirect, request
lab1 = Blueprint('lab1', __name__)

import datetime

not_found_log = [] # глобальный список для хранения журнала 404

@lab1.route("/bad_request")  # 400 Bad Request
def bad_request():
    return '''
<!doctype html>
<html>
    <body>
        <h1>400 — Bad Request</h1>
        <p>Неверный запрос: сервер не может обработать его из-за ошибки клиента.</p>
    </body>
</html>
''', 400


@lab1.route("/unauthorized") # 401 Unauthorized
def unauthorized():
    return '''
<!doctype html>
<html>
    <body>
        <h1>401 — Unauthorized</h1>
        <p>Требуется аутентификация: доступ запрещён без авторизации.</p>
    </body>
</html>
''', 401


@lab1.route("/payment_required") # 402 Payment Required
def payment_required():
    return '''
<!doctype html>
<html>
    <body>
        <h1>402 — Payment Required</h1>
        <p>Доступ ограничен: требуется оплата для получения ресурса.</p>
    </body>
</html>
''', 402


@lab1.route("/forbidden")    # 403 Forbidden
def forbidden():
    return '''
<!doctype html>
<html>
    <body>
        <h1>403 — Forbidden</h1>
        <p>Запрещено: у клиента нет прав доступа к содержимому.</p>
    </body>
</html>
''', 403


@lab1.route("/method_not_allowed")   # 405 Method Not Allowed
def method_not_allowed():
    return '''
<!doctype html>
<html>
    <body>
        <h1>405 — Method Not Allowed</h1>
        <p>Метод запроса запрещён для данного ресурса.</p>
    </body>
</html>
''', 405


@lab1.route("/teapot")   # 418 I'm a teapot
def teapot():
    return '''
<!doctype html>
<html>
    <body>
        <h1>418 — I'm a teapot</h1>
        <p>Сервер отказывается заваривать кофе, потому что он чайник 🫖.</p>
    </body>
</html>
''', 418


@lab1.route("/cause_error")
def cause_error():
    # Искусственная ошибка для демонстрации перехватчика
    return 1 / 0  # вызовет ZeroDivisionError


@lab1.route("/lab1") # лаба 1
def lab():
    return '''
<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Лабораторная 1</title>
    </head>
    <body>
        <h2>Лабораторная работа №1</h2>
        <p>
            Flask — фреймворк для создания веб-приложений на языке программирования Python,
            использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2.
            Относится к категории так называемых микрофреймворков —
            минималистичных каркасов веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
        </p>
        <hr>
        <a href="/">На главную</a>

        <h2>Список роутов</h2>
        <ul>
            <li><a href="/lab1/web">/lab1/web</a></li>
            <li><a href="/lab1/author">/lab1/author</a></li>
            <li><a href="/lab1/image">/lab1/image</a></li>
            <li><a href="/lab1/counter">/lab1/counter</a></li>
            <li><a href="/reset_counter">/reset_counter</a></li>
            <li><a href="/lab1/info">/lab1/info</a></li>
            <li><a href="/created">/created</a></li>
            <li><a href="/bad_request">/bad_request</a></li>
            <li><a href="/unauthorized">/unauthorized</a></li>
            <li><a href="/payment_required">/payment_required</a></li>
            <li><a href="/forbidden">/forbidden</a></li>
            <li><a href="/method_not_allowed">/method_not_allowed</a></li>
            <li><a href="/teapot">/teapot</a></li>
            <li><a href="/cause_error">/cause_error</a></li>
        </ul>
    </body>
</html>
'''


@lab1.route("/lab1/web")
def web():
    return """<!doctype html>
    	<html>
        	<body>
        		<h1>web-сервер на flask<h1>
                <a href="/lab1/author">author</a> <!-- Ссылка на /lab1/author -->
        	<body>
        <html>""", 200, {
            "X-Server": "sample",
            'Content-Type': 'text/plain; charset=utf-8'
        }


@lab1.route("/lab1/author")
def author():
    name = "Анчугова Софья Алексеевна" # Создание переменной name и присвоение ей значения с ФИО студента
    group = "ФБИ-32"  # Создание переменной group и присвоение ей значения с номером группы
    faculty = "ФБ" # Создание переменной faculty и присвоение ей значения с названием факультета

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/lab1/web">web</a> <!-- Ссылка на /lab1/web -->
            </body>
        </html>"""


@lab1.route('/lab1/image')
def image():
    path = url_for("static", filename="lab1/oak.jpg")
    css = url_for("static", filename="lab1/lab1.css")
    html_content = f'''
<!doctype html> 
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="{css}"> <!-- подключаем стили CSS -->
    </head>
    <body>
        <h1>Дуб</h1>
        <img src="{path}">
    </body>
</html>'''

    return html_content, 200, {
        "Content-Language": "ru",
        "X-Author": "Anchugova Sofya",
        "X-Lab": "Lab1-Image"
    }


count=0

@lab1.route('/lab1/counter')
def counter():
    global count
    count+=1
    time = datetime.datetime.today()    # текущую дату и время
    url = request.url                   # IP-адрес клиента
    client_ip = request.remote_addr     # имя хоста веб-сервера

    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <hr>
        Датаивремя: ''' + str(time) + '''<br>
        Запрошенный адрес: ''' + url + '''<br>
        ВашIP-адрес: ''' + client_ip + '''<br>
        <hr>
        <a href="/reset_counter">Очистить счётчик</a> <!-- ссылка на сброс -->
    </body>
</html> '''


@lab1.route('/reset_counter')
def reset_counter():
    global count
    count = 0  # обнуляем счётчик
    return '''
<!doctype html>
<html>
    <body>
        <h1>Счётчик очищен!</h1>
        <a href="/lab1/counter">Вернуться к счётчику</a>
    </body>
</html> '''


@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")


@lab1.route("/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html> ''', 201
