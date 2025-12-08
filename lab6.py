from flask import Blueprint, render_template, request, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

lab6 = Blueprint('lab6', __name__)

# ------------------------
# Универсальное подключение к БД
# ------------------------
def db_connect():
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
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur


def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


# ------------------------
# Основные маршруты
# ------------------------
@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')


@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']
    method = data['method']

    conn, cur = db_connect()

    # ------------------------
    # Метод info — список офисов
    # ------------------------
    if method == 'info':
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM offices ORDER BY number;")
        else:
            cur.execute("SELECT * FROM offices ORDER BY number;")

        offices = [dict(row) for row in cur.fetchall()]
        db_close(conn, cur)
        return {"jsonrpc": "2.0", "result": offices, "id": id}

    # Проверка авторизации
    login = session.get('login')
    if not login:
        db_close(conn, cur)
        return {"jsonrpc": "2.0", "error": {"code": 1, "message": "Unauthorized"}, "id": id}

    # ------------------------
    # Бронирование кабинета
    # ------------------------
    if method == 'booking':
        office_number = data['params']
        query = "SELECT tenant FROM offices WHERE number=" + ("%s" if current_app.config['DB_TYPE']=='postgres' else "?")
        cur.execute(query, (office_number,))
        office = cur.fetchone()

        if not office:
            db_close(conn, cur)
            return {"jsonrpc": "2.0", "error": {"code": -32000, "message": "Office not found"}, "id": id}

        if office['tenant']:
            db_close(conn, cur)
            return {"jsonrpc": "2.0", "error": {"code": 2, "message": "Already booked"}, "id": id}

        # обновляем аренду
        query = "UPDATE offices SET tenant=" + ("%s" if current_app.config['DB_TYPE']=='postgres' else "?") + " WHERE number=" + ("%s" if current_app.config['DB_TYPE']=='postgres' else "?")
        cur.execute(query, (login, office_number))
        db_close(conn, cur)
        return {"jsonrpc": "2.0", "result": "success", "id": id}

    # ------------------------
    # Отмена аренды
    # ------------------------
    if method == 'cancellation':
        office_number = data['params']
        query = "SELECT tenant FROM offices WHERE number=" + ("%s" if current_app.config['DB_TYPE']=='postgres' else "?")
        cur.execute(query, (office_number,))
        office = cur.fetchone()

        if not office:
            db_close(conn, cur)
            return {"jsonrpc": "2.0", "error": {"code": -32000, "message": "Office not found"}, "id": id}

        if not office['tenant']:
            db_close(conn, cur)
            return {"jsonrpc": "2.0", "error": {"code": 3, "message": "Офис не арендован"}, "id": id}

        if office['tenant'] != login:
            db_close(conn, cur)
            return {"jsonrpc": "2.0", "error": {"code": 4, "message": "Вы можете снять только свою аренду"}, "id": id}

        query = "UPDATE offices SET tenant=" + ("%s" if current_app.config['DB_TYPE']=='postgres' else "?") + " WHERE number=" + ("%s" if current_app.config['DB_TYPE']=='postgres' else "?")
        cur.execute(query, (None, office_number))
        db_close(conn, cur)
        return {"jsonrpc": "2.0", "result": "success", "id": id}

    # ------------------------
    # Общая стоимость аренды
    # ------------------------
    if method == 'total':
        query = "SELECT SUM(price) as total FROM offices WHERE tenant=" + ("%s" if current_app.config['DB_TYPE']=='postgres' else "?")
        cur.execute(query, (login,))
        total = cur.fetchone()['total'] or 0
        db_close(conn, cur)
        return {"jsonrpc": "2.0", "result": total, "id": id}

    # ------------------------
    # Неизвестный метод
    # ------------------------
    db_close(conn, cur)
    return {"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}, "id": id}
