import datetime
import os
from os import path
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from db import db
from db.models import users

from flask import Flask, url_for, request
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
from lab9 import lab9
from rgz import rgz

app = Flask(__name__)

# Инициализация логин-менеджера
login_manager = LoginManager()
login_manager.login_view = 'lab8.login'
login_manager.init_app(app)

@login_manager.user_loader      # Указание, где брать пользователей
def load_users(login_id):
    return users.query.get(int(login_id))

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный секрет') 
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

if app.config['DB_TYPE'] == 'postgres':
    db_name = 'sonya_anchugova_orm'
    db_user = 'sonya_anchugova_orm'
    db_password = '123'
    host_ip = '127.0.0.1'
    host_port = 5432

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
else:
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "sonya_anchugova_orm.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db.init_app(app)

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)
app.register_blueprint(lab9)
app.register_blueprint(rgz)

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
            <li><a href="/lab4/">Четвертая лабораторная</a></li>            
            <li><a href="/lab5/">Пятая лабораторная</a></li>
            <li><a href="/lab6/">Шестая лабораторная</a></li>
            <li><a href="/lab7/">Седьмая лабораторная</a></li>
            <li><a href="/lab8/">Восьмая лабораторная</a></li>
            <li><a href="/lab9/">Девятая лабораторная</a></li>
            <li><a href="/rgz/">РГЗ</a></li>
        </ul>
        <hr>
        <footer>
            Анчугова Софья Алексеевна, ФБИ-32, 3 курс, 2025
        </footer>
    </body>
</html>
'''
