from flask import Blueprint, render_template, request, redirect, session
import psycopg2
from psycopg2.extras import RealDictCursor

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    login = session.get('login', 'Anonymous')  # если пользователь не вошёл, показываем "Anonymous"
    return render_template('lab5/lab5.html', login=login)

def bd_connect():
    conn = psycopg2.connect(
        host = '127.0.0.1',
        database = 'sonya_anchugova_knowledge_base',
        user = 'sonya_anchugova_knowledge_base',
        password = 'sonya'
    )
    cur = conn.cursor(cursor_factory = RealDictCursor)      #RealDictCursor - чтобы образаться к полям записей по именам столбцов

    return conn, cur

def bd_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()



@lab5.route('/lab5/register', methods = ['GET', 'POST'])    # для метода get показывал форму аутентификации; для метода post запускал процедуру регистрации
def register():
    if request.method == 'GET':     
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/register.html', error='Заполните все поля')
    
    conn, cur = bd_connect()

    cur.execute(f"SELECT login FROM users WHERE login='{login}';")  #сделаем SQL-запрос к БД, поищем пользователя с введённым логином
    if cur.fetchone():
        bd_close(conn, cur)
        return render_template('lab5/register.html', error="Такой пользователь уже существует")
    
    cur.execute(f"INSERT INTO users (login, password) VALUES ('{login}', '{password}');")   #регистрируем пользователя, вставляя в таблицу логин и пароль
    
    bd_close(conn, cur)
    return render_template('lab5/success.html', login=login)


@lab5.route('/lab5/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    
    if not (login or password):
        return render_template('lab5/login.html', error="Заполните поля")
    
    conn, cur = bd_connect()
    
    cur.execute(f"SELECT * FROM users WHERE login='{login}';")      #Поиск пользователя в БД
    user = cur.fetchone()

    if not user:
        bd_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')
    
    if user['password'] != password:     #Если найден пользователь, но пароль не совпадает
        bd_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')
    
    session['login'] = login       #для хранения данных аутентификации; теперь в сессии будет храниться логин пользователя 
    bd_close(conn, cur)
    return render_template('lab5/success_login.html', login=login)      #вход в сиситему, если все правильно


@lab5.route('/lab5/list')
def list_articles():
    return render_template('lab5/list.html')


@lab5.route('/lab5/create')
def create_article():
    return render_template('lab5/create.html')
