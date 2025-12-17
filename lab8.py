from flask import Blueprint, render_template, request, abort, jsonify, current_app, session
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

lab8 = Blueprint('lab8', __name__)


def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host = '127.0.0.1',
            database = 'sonya_anchugova_knowledge_base',
            user = 'sonya_anchugova_knowledge_base',
            password = 'sonya'
        )
        cur = conn.cursor(cursor_factory = RealDictCursor)
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


@lab8.route('/lab8/')
def lab():
    login = session.get('login', 'Anonymous')
    return render_template('lab8/lab8.html', login=login)


@lab8.route('/lab8/login')
def login():
    return "Страница входа (будет реализована позже)"


@lab8.route('/lab8/register')
def register():
    return "Страница регистрации (будет реализована позже)"


@lab8.route('/lab8/articles')
def articles():
    return "Список статей (будет реализован позже)"


@lab8.route('/lab8/create')
def create():
    return "Создание статьи (будет реализовано позже)"




