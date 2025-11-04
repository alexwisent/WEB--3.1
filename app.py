import datetime
from flask import Flask, url_for, request
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3


app = Flask(__name__)
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)

not_found_log = [] # глобальный список для хранения журнала 404

@app.errorhandler(404) #перехват ошибки
def not_found(err):
    client_ip = request.remote_addr
    access_time = datetime.datetime.now()
    requested_url = request.url

    # добавляем запись в журнал
    not_found_log.append((access_time, client_ip, requested_url))

    # путь к CSS
    css_path = url_for('static', filename='lab1.css')
    
    # формируем HTML для журнала
    log_html = ""
    for entry in not_found_log:
        log_html += f"<li>[{entry[0]}, пользователь {entry[1]}] зашёл на адрес: {entry[2]}</li>\n"

    return f'''
<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Страница не найдена</title>
        <link rel="stylesheet" type="text/css" href="{css_path}">
    </head>
    <body class="error404">
        <h1>404 — Страница не найдена</h1>
        <p>Упс! Кажется, вы заблудились.</p>
        <p>Ваш IP: {client_ip}</p>
        <p>Дата и время доступа: {access_time}</p>
        <a href="/">Вернуться на главную</a>

        <div class="log">
            <h2>Журнал посещений несуществующих страниц:</h2>
            <ul>
                {log_html}
            </ul>
        </div>
    </body>
</html>
''', 404


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
@app.route("/start")
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
            <li><a href="/lab2/">Вторая лабораторная</a></li>
            <li><a href="/lab3/">Третья лабораторная</a></li>
        </ul>
        <hr>
        <footer>
            Анчугова Софья Алексеевна, ФБИ-32, 3 курс, 2025
        </footer>
    </body>
</html>
'''

