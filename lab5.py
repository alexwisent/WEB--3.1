from flask import Blueprint, render_template, request, redirect, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    login = session.get('login', 'Anonymous')  # если пользователь не вошёл, показываем "Anonymous"
    return render_template('lab5/lab5.html', login=login)


def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host = '127.0.0.1',
            database = 'sonya_anchugova_knowledge_base',
            user = 'sonya_anchugova_knowledge_base',
            password = 'sonya'
        )
        cur = conn.cursor(cursor_factory = RealDictCursor)      #RealDictCursor - чтобы образаться к полям записей по именам столбцов
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row      #чтобы получать отдельные поля записей по ключу, а не по номеру
        cur = conn.cursor()

    return conn, cur


def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    full_name = request.form.get('full_name', '')  # Получаем полное имя, по умолчанию пустая строка

    if not login or not password:
        return render_template('lab5/register.html', error='Заполните все обязательные поля', full_name=full_name)
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login,))

    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', error="Такой пользователь уже существует", full_name=full_name)

    password_hash = generate_password_hash(password)

    # Вставляем пользователя с полным именем
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password, full_name) VALUES (%s, %s, %s);", 
                   (login, password_hash, full_name))
    else:
        cur.execute("INSERT INTO users (login, password, full_name) VALUES (?, ?, ?);", 
                   (login, password_hash, full_name))

    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)


@lab5.route('/lab5/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    
    if not (login or password):
        return render_template('lab5/login.html', error="Заполните поля")
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))    #Поиск пользователя в БД
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))

    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')
    
    if not check_password_hash(user['password'], password):     #Если найден пользователь, но пароль не совпадает
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')
    
    session['login'] = login       #для хранения данных аутентификации; теперь в сессии будет храниться логин пользователя 
    db_close(conn, cur)
    return render_template('lab5/success_login.html', login=login)      #вход в сиситему, если все правильно


@lab5.route('/lab5/list')
def list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))

    login_id = cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE user_id=%s;", (login_id,))
    else:
        cur.execute("SELECT * FROM articles WHERE user_id=?;", (login_id,))

    articles = cur.fetchall()

    db_close(conn, cur)
    return render_template('/lab5/articles.html', articles=articles)


@lab5.route('/lab5/create', methods = ['GET', 'POST'])
def create_article():
    login=session.get('login')
    if not login:
        return redirect('/lab5/login')

    if request.method == 'GET':
        return render_template('lab5/create_article.html')      #покажем страницу ввода статьи
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')

    # Валидация: проверяем, что поля не пустые
    if not title or not article_text:
        error = "Пожалуйста, заполните название и текст статьи"
        return render_template('lab5/create_article.html', error=error, title=title, article_text=article_text)

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))

    login_id = cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO articles (user_id, title, article_text) VALUES (%s, %s, %s);", (login_id, title, article_text))
    else:
        cur.execute("INSERT INTO articles (user_id, title, article_text) VALUES (?, ?, ?);", (login_id, title, article_text))

    db_close(conn, cur)
    return redirect('/lab5') #или /lab5/


@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    # Получаем ID пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    login_id = cur.fetchone()["id"]

    # Получаем статью
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s AND user_id=%s;", (article_id, login_id))
    else:
        cur.execute("SELECT * FROM articles WHERE id=? AND user_id=?;", (article_id, login_id))
    article = cur.fetchone()

    if not article:
        db_close(conn, cur)
        return "Статья не найдена или у вас нет доступа"

    if request.method == 'POST':
        title = request.form.get('title')
        article_text = request.form.get('article_text')

        if not title or not article_text:
            error = "Пожалуйста, заполните название и текст статьи"
            return render_template('lab5/edit_article.html', article=article, error=error)

        # Обновление
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE articles SET title=%s, article_text=%s WHERE id=%s;", (title, article_text, article_id))
        else:
            cur.execute("UPDATE articles SET title=?, article_text=? WHERE id=?;", (title, article_text, article_id))

        db_close(conn, cur)
        return redirect('/lab5/list')

    db_close(conn, cur)
    return render_template('lab5/edit_article.html', article=article)


@lab5.route('/lab5/delete/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    # Получаем ID пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    login_id = cur.fetchone()["id"]

    # Удаляем только если статья принадлежит пользователю
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM articles WHERE id=%s AND user_id=%s;", (article_id, login_id))
    else:
        cur.execute("DELETE FROM articles WHERE id=? AND user_id=?;", (article_id, login_id))

    db_close(conn, cur)
    return redirect('/lab5/list')


@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)  # удаляем логин из сессии
    return redirect('/lab5/login')


@lab5.route('/lab5/users')
def show_users():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    # Получаем всех пользователей (без паролей)
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login, full_name FROM users ORDER BY login;")
    else:
        cur.execute("SELECT login, full_name FROM users ORDER BY login;")
    
    users = cur.fetchall()
    
    db_close(conn, cur)
    return render_template('lab5/users.html', users=users)


@lab5.route('/lab5/change_profile', methods=['GET', 'POST'])
def change_profile():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    if request.method == 'GET':
        # Получаем текущие данные пользователя
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT login, full_name FROM users WHERE login=%s;", (login,))
        else:
            cur.execute("SELECT login, full_name FROM users WHERE login=?;", (login,))
        
        user = cur.fetchone()
        current_login = user['login'] if user else login
        current_full_name = user['full_name'] if user else ''
        
        db_close(conn, cur)
        return render_template('lab5/change_profile.html', 
                             current_login=current_login,
                             current_full_name=current_full_name)
    
    # Обработка POST запроса
    new_login = request.form.get('login')
    new_full_name = request.form.get('full_name', '')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    errors = []
    success_message = None
    
    # Проверка обязательных полей
    if not new_login:
        errors.append("Логин не может быть пустым")
    
    # Проверка уникальности нового логина (если он изменился)
    if new_login != login:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT login FROM users WHERE login=%s;", (new_login,))
        else:
            cur.execute("SELECT login FROM users WHERE login=?;", (new_login,))
        
        if cur.fetchone():
            errors.append(f"Логин '{new_login}' уже занят")
    
    # Проверка пароля
    if new_password:
        if new_password != confirm_password:
            errors.append("Новый пароль и подтверждение не совпадают")
    
    if not errors:
        # Обновляем данные
        try:
            if new_password:
                # Если меняем пароль
                password_hash = generate_password_hash(new_password)
                if current_app.config['DB_TYPE'] == 'postgres':
                    cur.execute("UPDATE users SET login=%s, full_name=%s, password=%s WHERE login=%s;",
                              (new_login, new_full_name, password_hash, login))
                else:
                    cur.execute("UPDATE users SET login=?, full_name=?, password=? WHERE login=?;",
                              (new_login, new_full_name, password_hash, login))
                
                if new_login != login:
                    # Обновляем сессию, если логин изменился
                    session['login'] = new_login
                    success_message = f"Логин, имя и пароль успешно изменены! Новый логин: {new_login}"
                else:
                    success_message = "Имя и пароль успешно изменены!"
            else:
                # Если не меняем пароль
                if current_app.config['DB_TYPE'] == 'postgres':
                    cur.execute("UPDATE users SET login=%s, full_name=%s WHERE login=%s;",
                              (new_login, new_full_name, login))
                else:
                    cur.execute("UPDATE users SET login=?, full_name=? WHERE login=?;",
                              (new_login, new_full_name, login))
                
                if new_login != login:
                    # Обновляем сессию, если логин изменился
                    session['login'] = new_login
                    success_message = f"Логин и имя успешно изменены! Новый логин: {new_login}"
                else:
                    success_message = "Имя успешно изменено!"
            
            db_close(conn, cur)
            
            # После успешного обновления получаем обновленные данные для формы
            conn, cur = db_connect()
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("SELECT login, full_name FROM users WHERE login=%s;", (session['login'],))
            else:
                cur.execute("SELECT login, full_name FROM users WHERE login=?;", (session['login'],))
            
            user = cur.fetchone()
            current_login = user['login'] if user else session['login']
            current_full_name = user['full_name'] if user else ''
            
            db_close(conn, cur)
            return render_template('lab5/change_profile.html', 
                                 current_login=current_login,
                                 current_full_name=current_full_name,
                                 success_message=success_message)
            
        except Exception as e:
            errors.append(f"Ошибка при обновлении данных: {str(e)}")
    
    # Если есть ошибки или нужно просто показать форму
    db_close(conn, cur)
    return render_template('lab5/change_profile.html',
                         errors=errors,
                         current_login=new_login,
                         current_full_name=new_full_name)