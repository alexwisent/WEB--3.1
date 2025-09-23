from flask import Flask, url_for, request, redirect 
import datetime
app = Flask(__name__)

# коды ответов
# 404 error
@app.errorhandler(404)
def not_found(err):
    img_path = url_for('static', filename='404.png')
    css_path = url_for('static', filename='lab1.css')
    return '''
<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Страница не найдена</title>
        <link rel="stylesheet" type="text/css" href="''' + css_path + '''">
    </head>
    <body class="error404">
        <h1>404 — Страница не найдена</h1>
        <p>Упс! Кажется, вы заблудились.</p>
        <img src="''' + img_path + '''" alt="404">
        <br>
        <a href="/">Вернуться на главную</a>
    </body>
</html>
''', 404

# 400 Bad Request
@app.route("/bad_request")
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


# 401 Unauthorized
@app.route("/unauthorized")
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


# 402 Payment Required
@app.route("/payment_required")
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


# 403 Forbidden
@app.route("/forbidden")
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


# 405 Method Not Allowed
@app.route("/method_not_allowed")
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


# 418 I'm a teapot
@app.route("/teapot")
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

@app.route("/cause_error")
def cause_error():
    # Искусственная ошибка для демонстрации перехватчика
    return 1 / 0  # вызовет ZeroDivisionError

@app.errorhandler(500)
def handle_500_error(err):
    css_path = url_for('static', filename='lab1.css')  # общий CSS
    return '''
<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Ошибка на сервере</title>
        <link rel="stylesheet" type="text/css" href="''' + css_path + '''">
    </head>
    <body class="error500">
        <h1>500 — Внутренняя ошибка сервера</h1>
        <p>Упс! На сервере произошла непредвиденная ошибка.</p>
        <br>
        <a href="/">Вернуться на главную</a>
    </body>
</html>
''', 500





# главная страница
@app.route("/")
@app.route("/index")
def index():
    return '''
<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        <hr>
        <ul>
            <li><a href="/lab1">Первая лабораторная</a></li>
        </ul>
        <hr>
        <footer>
            Анчугова Софья Алексеевна, ФБИ-32, 3 курс, 2025
        </footer>
    </body>
</html>
'''

# лаба 1
@app.route("/lab1")
def lab1():
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
    </body>
</html>
'''



@app.route("/lab1/web")
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


@app.route("/lab1/author")
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


@app.route('/lab1/image')
def image():
    path = url_for("static", filename="oak.jpg")
    css = url_for("static", filename="lab1.css")
    return '''
<!doctype html> 
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + css + '''"> <!-- подключаем стили сss -->
    </head>
    <body>
        <h1>Дуб</h1>
        <img src="''' + path + '''">
    </body>
</html> '''


count=0

@app.route('/lab1/counter')
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


@app.route('/reset_counter')
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


@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")


@app.route("/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html> ''', 201


