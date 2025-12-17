from flask import Blueprint, render_template, request, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

lab6 = Blueprint('lab6', __name__)

def db_connect():       # Подключаемся к PostgreSQL или SQLite в зависимости от конфигурации
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='sonya_anchugova_knowledge_base',
            user='sonya_anchugova_knowledge_base',
            password='sonya'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row      # Для получения строк в виде словарей
        cur = conn.cursor()

    return conn, cur


def db_close(conn, cur):        # Функция закрытия соединения с БД
    conn.commit()       # Сохраняем изменения
    cur.close()         # Закрываем курсор
    conn.close()        # Закрываем соединение


# ------------------------
# Основные маршруты
# ------------------------
@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')    # Отображаем главную страницу лабораторной работы


@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']
    method = data['method']

    conn, cur = db_connect()        # Устанавливаем соединение с БД

    if method == 'info':        # получение списка всех офисов
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM offices ORDER BY number;")
        else:
            cur.execute("SELECT * FROM offices ORDER BY number;")

        offices = [dict(row) for row in cur.fetchall()]     # Преобразуем в словари
        db_close(conn, cur)
        return {"jsonrpc": "2.0", "result": offices, "id": id}

    login = session.get('login')        # Проверка авторизации пользователя
    if not login:
        db_close(conn, cur)
        return {"jsonrpc": "2.0", "error": {"code": 1, "message": "Unauthorized"}, "id": id}

    if method == 'booking':     # Бронирование кабинета
        office_number = data['params']      # Номер офиса для бронирования
        query = "SELECT tenant FROM offices WHERE number=" + ("%s" if current_app.config['DB_TYPE']=='postgres' else "?")   # Проверяем существование офиса
        cur.execute(query, (office_number,))
        office = cur.fetchone()

        if not office:  
            db_close(conn, cur)
            return {"jsonrpc": "2.0", "error": {"code": -32000, "message": "Office not found"}, "id": id}

        if office['tenant']:    # Проверяем, не занят ли уже офис
            db_close(conn, cur)
            return {"jsonrpc": "2.0", "error": {"code": 2, "message": "Already booked"}, "id": id}

        # Бронируем офис для текущего пользователя
        query = "UPDATE offices SET tenant=" + ("%s" if current_app.config['DB_TYPE']=='postgres' else "?") + " WHERE number=" + ("%s" if current_app.config['DB_TYPE']=='postgres' else "?")
        cur.execute(query, (login, office_number))
        db_close(conn, cur)
        return {"jsonrpc": "2.0", "result": "success", "id": id}

    if method == 'cancellation':        # Отмена аренды
        office_number = data['params']  # Номер офиса для освобождения
        query = "SELECT tenant FROM offices WHERE number=" + ("%s" if current_app.config['DB_TYPE']=='postgres' else "?")       # Проверяем, существует ли офис
        cur.execute(query, (office_number,))
        office = cur.fetchone()

        if not office:
            db_close(conn, cur)
            return {"jsonrpc": "2.0", "error": {"code": -32000, "message": "Office not found"}, "id": id}

        if not office['tenant']:    # Проверяем, арендован ли офис
            db_close(conn, cur)
            return {"jsonrpc": "2.0", "error": {"code": 3, "message": "Офис не арендован"}, "id": id}

        if office['tenant'] != login:   # Проверяем, может ли пользователь снять аренду (только свою)
            db_close(conn, cur)
            return {"jsonrpc": "2.0", "error": {"code": 4, "message": "Вы можете снять только свою аренду"}, "id": id}

        # Освобождаем офис (устанавливаем tenant в NULL)
        query = "UPDATE offices SET tenant=" + ("%s" if current_app.config['DB_TYPE']=='postgres' else "?") + " WHERE number=" + ("%s" if current_app.config['DB_TYPE']=='postgres' else "?")
        cur.execute(query, (None, office_number))
        db_close(conn, cur)
        return {"jsonrpc": "2.0", "result": "success", "id": id}

    if method == 'total':       # Общая стоимость аренды
        query = "SELECT SUM(price) as total FROM offices WHERE tenant=" + ("%s" if current_app.config['DB_TYPE']=='postgres' else "?")
        cur.execute(query, (login,))
        total = cur.fetchone()['total'] or 0
        db_close(conn, cur)
        return {"jsonrpc": "2.0", "result": total, "id": id}

    db_close(conn, cur)     # Неизвестный метод
    return {"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}, "id": id}

