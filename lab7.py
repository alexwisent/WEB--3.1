from flask import Blueprint, render_template, request, abort, jsonify, current_app
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

lab7 = Blueprint('lab7', __name__)

def db_connect():       # Подключение к базе данных в зависимости от типа БД
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


def db_close(conn, cur):    # Закрытие соединения с БД
    conn.commit()
    cur.close()
    conn.close()


def init_db():      # Инициализация базы данных с начальными данными
    conn, cur = db_connect()
    
    try:
        if current_app.config['DB_TYPE'] == 'postgres':     # Проверяем, есть ли уже данные в таблице
            cur.execute("SELECT COUNT(*) as count FROM films")
        else:
            cur.execute("SELECT COUNT(*) as count FROM films")
        
        result = cur.fetchone()
        count = result['count'] if isinstance(result, dict) else result[0]      # Извлекаем количество записей в зависимости от типа БД
        
        if count == 0:      # Если таблица пуста, добавляем начальные данные
            films = [
                {
                    "title": "E.T. the Extra-Terrestrial",
                    "title_ru": "Инопланетянин",
                    "year": 1982,
                    "description": "Семейный научно‑фантастический фильм Стивена Спилберга о дружбе мальчика и дружелюбного пришельца. Картина преодолела скептицизм продюсеров и стала кассовым хитом (сборы — 663,4 млн долларов), изменив представление о «хороших инопланетянах» в кино. Фильм затрагивает темы «американской мечты», политики и популярной культуры США второй половины XX века."
                },
                {
                    "title": "Jurassic Park",
                    "title_ru": "Парк Юрского периода",
                    "year": 1993,
                    "description": "Фильм Стивена Спилберга, который задал новый стандарт использования компьютерной графики в кино. История о парке с живыми динозаврами, где эксперимент выходит из‑под контроля. Собрал 912,6 млн долларов в прокате, вдохновил последующие поколения режиссёров (Питера Джексона, Джорджа Лукаса) и положил начало долгоиграющей франшизе."
                },
                {
                    "title": "Star Wars: Episode I – The Phantom Menace",
                    "title_ru": "Звёздные войны: Эпизод I – Скрытая угроза",
                    "year": 1999,
                    "description": "Приквел космической саги «Звёздные войны», собравший 1 млрд 27 млн долларов. Фильм стал технологическим прорывом — для него создали первую профессиональную цифровую камеру. Режиссёр Джордж Лукас вплетёт в повествование отсылки к самурайской культуре, китайским боевым искусствам, Библии и мифологическим архетипам, сохраняя семейный формат франшизы."
                },
                {
                    "title": "Titanic",
                    "title_ru": "Титаник",
                    "year": 1997,
                    "description": "Эпическая мелодрама Джеймса Кэмерона о крушении лайнера в 1912 году. При бюджете 200 млн долларов фильм собрал 2 млрд 264 млн, став самым кассовым в истории на 12 лет. Получил 11 премий «Оскар», включая «Лучший фильм». История любви Джека и Розы на фоне катастрофы, саундтрек My Heart Will Go On и визуальные эффекты сделали картину культовой."
                },
                {
                    "title": "The Substance",
                    "title_ru": "Субстанция",
                    "year": 2024,
                    "description": "Боди‑хоррор режиссёра Корали Фаржа с Деми Мур и Маргарет Куолли. История стареющей телезвезды Элизабет, которая принимает препарат «Субстанция», создающий её молодую копию — Сью. Фильм получил награду за лучший сценарий на Каннском фестивале-2024. Исследует темы самопринятия, нереалистичных стандартов красоты и разрушительных последствий раздвоения личности."
                },
            ]
            
            for film in films:
                if current_app.config['DB_TYPE'] == 'postgres':
                    cur.execute(
                        "INSERT INTO films (title, title_ru, year, description) VALUES (%s, %s, %s, %s)",
                        (film['title'], film['title_ru'], film['year'], film['description'])
                    )
                else:
                    cur.execute(
                        "INSERT INTO films (title, title_ru, year, description) VALUES (?, ?, ?, ?)",
                        (film['title'], film['title_ru'], film['year'], film['description'])
                    )
            
            conn.commit()
            print(f"Добавлено {len(films)} фильмов в БД")
    except Exception as e:
        print(f"Ошибка при инициализации БД: {e}")
        conn.rollback()
    finally:
        db_close(conn, cur)


@lab7.route('/lab7/')
def main(): # При загрузке страницы проверяем и инициализируем БД
    init_db()
    return render_template('lab7/lab7.html')


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn, cur = db_connect()
    
    try:
        cur.execute("SELECT id, title, title_ru, year, description FROM films ORDER BY id")     # Получаем все фильмы из БД, отсортированные по ID
        films = cur.fetchall()
        
        result = []     # Преобразуем в список словарей
        for film in films:
            if isinstance(film, dict):
                result.append(film)     # PostgreSQL уже возвращает словарь
            else:
                result.append(dict(film))       # SQLite: преобразуем Row в словарь
        
        return jsonify(result)
    except Exception as e:
        print(f"Ошибка при получении фильмов: {e}")
        return jsonify({"error": "Ошибка при получении фильмов"}), 500
    finally:
        db_close(conn, cur)


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn, cur = db_connect()
    
    try:
        if current_app.config['DB_TYPE'] == 'postgres':     # Получаем фильм по ID
            cur.execute("SELECT id, title, title_ru, year, description FROM films WHERE id = %s", (id,))
        else:
            cur.execute("SELECT id, title, title_ru, year, description FROM films WHERE id = ?", (id,))
        
        film = cur.fetchone()
        
        if film:        # Возвращаем найденный фильм
            if isinstance(film, dict):
                return jsonify(film)
            else:
                return jsonify(dict(film))
        else:
            abort(404, description="Фильм с таким id не найден")
    except Exception as e:
        print(f"Ошибка при получении фильма: {e}")
        abort(500, description="Внутренняя ошибка сервера")
    finally:
        db_close(conn, cur)


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    conn, cur = db_connect()
    
    try:
        if current_app.config['DB_TYPE'] == 'postgres':     # Сначала проверяем существование фильма
            cur.execute("SELECT id FROM films WHERE id = %s", (id,))
        else:
            cur.execute("SELECT id FROM films WHERE id = ?", (id,))
        
        if not cur.fetchone():
            abort(404, description="Фильм с таким id не найден")
        
        if current_app.config['DB_TYPE'] == 'postgres':     # Удаляем фильм
            cur.execute("DELETE FROM films WHERE id = %s", (id,))
        else:
            cur.execute("DELETE FROM films WHERE id = ?", (id,))
        
        conn.commit()       # Сохраняем удаление
        return '', 204
    except Exception as e:
        print(f"Ошибка при удалении фильма: {e}")
        abort(500, description="Внутренняя ошибка сервера")
    finally:
        db_close(conn, cur)


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):   # обновление существующего фильма
    conn, cur = db_connect()
    
    try:
        # Проверяем существование фильма
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id FROM films WHERE id = %s", (id,))
        else:
            cur.execute("SELECT id FROM films WHERE id = ?", (id,))
        
        if not cur.fetchone():
            abort(404, description="Фильм с таким id не найден")
        
        film = request.get_json()
        errors = {}
        
        # 1. Проверка русского названия (должно быть непустым)
        if not film.get('title_ru', '').strip():
            errors['title_ru'] = 'Введите русское название фильма'
        
        # 2. Проверка оригинального названия (должно быть непустым, если русское пустое)
        if not film.get('title_ru', '').strip() and not film.get('title', '').strip():
            errors['title'] = 'Введите оригинальное название, если русское название пустое'
        
        # 3. Проверка года (должен быть от 1895 до текущего)
        try:
            year = int(film.get('year', 0))
            current_year = datetime.now().year
            if year < 1895 or year > current_year:
                errors['year'] = f'Год должен быть от 1895 до {current_year}'
        except (ValueError, TypeError):
            errors['year'] = 'Год должен быть числом'
        
        # 4. Проверка описания (непустое и не более 2000 символов)
        description = film.get('description', '')
        if not description.strip():
            errors['description'] = 'Заполните описание'
        elif len(description) > 2000:
            errors['description'] = 'Описание не должно превышать 2000 символов'
        
        # Если есть ошибки, возвращаем их
        if errors:
            return jsonify(errors), 400
        
        # если оригинальное название пустое, используем русское
        if not film.get('title', '').strip() and film.get('title_ru', '').strip():
            film['title'] = film['title_ru']
        
        # Обновляем фильм в БД
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute(
                "UPDATE films SET title = %s, title_ru = %s, year = %s, description = %s WHERE id = %s",
                (film['title'], film['title_ru'], film['year'], film['description'], id)
            )
        else:
            cur.execute(
                "UPDATE films SET title = ?, title_ru = ?, year = ?, description = ? WHERE id = ?",
                (film['title'], film['title_ru'], film['year'], film['description'], id)
            )
        
        conn.commit()
        
        # Возвращаем обновленный фильм
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id, title, title_ru, year, description FROM films WHERE id = %s", (id,))
        else:
            cur.execute("SELECT id, title, title_ru, year, description FROM films WHERE id = ?", (id,))
        
        updated_film = cur.fetchone()
        if isinstance(updated_film, dict):
            return jsonify(updated_film)
        else:
            return jsonify(dict(updated_film))
            
    except Exception as e:
        print(f"Ошибка при обновлении фильма: {e}")
        conn.rollback()
        abort(500, description="Внутренняя ошибка сервера")
    finally:
        db_close(conn, cur)


@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    conn, cur = db_connect()
    
    try:
        film = request.get_json()
        errors = {}
        
        # 1. Проверка русского названия (должно быть непустым)
        if not film.get('title_ru', '').strip():
            errors['title_ru'] = 'Введите русское название фильма'
        
        # 2. Проверка оригинального названия (должно быть непустым, если русское пустое)
        if not film.get('title_ru', '').strip() and not film.get('title', '').strip():
            errors['title'] = 'Введите оригинальное название, если русское название пустое'
        
        # 3. Проверка года (должен быть от 1895 до текущего)
        try:
            year = int(film.get('year', 0))
            current_year = datetime.now().year
            if year < 1895 or year > current_year:
                errors['year'] = f'Год должен быть от 1895 до {current_year}'
        except (ValueError, TypeError):
            errors['year'] = 'Год должен быть числом'
        
        # 4. Проверка описания (непустое и не более 2000 символов)
        description = film.get('description', '')
        if not description.strip():
            errors['description'] = 'Заполните описание'
        elif len(description) > 2000:
            errors['description'] = 'Описание не должно превышать 2000 символов'
        
        # Если есть ошибки, возвращаем их
        if errors:
            return jsonify(errors), 400
        
        # Логика: если оригинальное название пустое, используем русское
        if not film.get('title', '').strip() and film.get('title_ru', '').strip():
            film['title'] = film['title_ru']
        
        # Добавляем фильм в БД
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute(
                "INSERT INTO films (title, title_ru, year, description) VALUES (%s, %s, %s, %s) RETURNING id",
                (film['title'], film['title_ru'], film['year'], film['description'])
            )
            new_id = cur.fetchone()['id']
        else:
            cur.execute(
                "INSERT INTO films (title, title_ru, year, description) VALUES (?, ?, ?, ?)",
                (film['title'], film['title_ru'], film['year'], film['description'])
            )
            new_id = cur.lastrowid
        
        conn.commit()
        return jsonify({"id": new_id}), 201
        
    except Exception as e:
        print(f"Ошибка при добавлении фильма: {e}")
        conn.rollback()
        abort(500, description="Внутренняя ошибка сервера")
    finally:
        db_close(conn, cur)