from flask import Blueprint, render_template, request, abort, jsonify
from datetime import datetime

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/lab7.html')


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


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify(films)  


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if 0 <= id < len(films):
        return jsonify(films[id])  
    else:
        abort(404, description="Фильм с таким id не найден")


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if 0 <= id < len(films):
        del films[id]
        return '', 204
    else:
        abort(404, description="Фильм с таким id не найден")


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if 0 <= id < len(films):
        film = request.get_json()
        errors = {}
        
        # 1. Проверка русского названия (должно быть непустым)
        if not film.get('title_ru', '').strip():
            errors['title_ru'] = 'Введите русское название фильма'
        
        # 2. Проверка оригинального названия (должно быть непустым, если русское пустое)
        if not film.get('title_ru', '').strip() and not film.get('title', '').strip():
            errors['title'] = 'Введите оригинальное название, если русское название пустое'
        
        # Если оба названия пустые, оригинальное не проверяем отдельно
        # Но если нужно оригинальное всегда непустое, когда русское пустое:
        if not film.get('title_ru', '').strip() and not film.get('title', '').strip():
            if 'title' not in errors:
                errors['title'] = 'Введите оригинальное название'
        
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
        
        films[id] = film
        return jsonify(films[id])
    else:
        abort(404, description="Фильм с таким id не найден")


@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    errors = {}
    
    # 1. Проверка русского названия (должно быть непустым)
    if not film.get('title_ru', '').strip():
        errors['title_ru'] = 'Введите русское название фильма'
    
    # 2. Проверка оригинального названия (должно быть непустым, если русское пустое)
    if not film.get('title_ru', '').strip() and not film.get('title', '').strip():
        errors['title'] = 'Введите оригинальное название, если русское название пустое'
    
    # Если оба названия пустые, оригинальное не проверяем отдельно
    # Но если нужно оригинальное всегда непустое, когда русское пустое:
    if not film.get('title_ru', '').strip() and not film.get('title', '').strip():
        if 'title' not in errors:
            errors['title'] = 'Введите оригинальное название'
    
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
    
    films.append(film)
    new_id = len(films) - 1
    return jsonify({"id": new_id}), 201

