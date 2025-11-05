from flask import Blueprint, url_for, redirect, render_template, abort, request
lab2 = Blueprint('lab2', __name__)
import datetime


@lab2.route('/lab2/a/') 
def a():
    return 'со слешем'

@lab2.route('/lab2/a') 
def a2():
    return 'без слеша'


# flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка'] # Определим список наших цветов как список чтобы можно было добавлять элементы

# @lab2.route('/lab2/flowers/<int:flower_id>')  # Обработчик динамического пути: <flower_id>
# def flowers(flower_id):
#     if flower_id >= len(flower_list): # len тянет именно колво элементов, а не индекс, поэтому >=
#         abort(404)
#     else:
#         # return "цветок: " + flower_list[flower_id]
#         flower = flower_list[flower_id]
#         return f'''
# <!doctype html>
# <html>
#     <body>
#         <h1>Информация о цветке</h1>
#         <p><b>ID:</b> {flower_id}</p>
#         <p><b>Название:</b> {flower}</p>
#         <hr>
#         <a href="/lab2/all_flowers">Посмотреть все цветы</a>
#     </body>
# </html>
# '''    


# @lab2.route('/lab2/add_flower/') # Добавление цветка с проверкой имени
# def add_flower_no_name():
#     # Если пользователь не указал имя
#     return '''
# <!doctype html>
# <html>
#     <body>
#         <h1>400 — Bad Request</h1>
#         <p>Не задано имя цветка :( </p>
#         <a href="/lab2/all_flowers">Посмотреть все цветы</a>
#     </body>
# </html>''', 400

# @lab2.route('/lab2/add_flower/<name>') # добавление цветка в список       #тип name по умолчанию string
# def add_flower(name): # берем имя из адреса 
#     flower_list.lab2end(name) # добавляем его в конец списка
#     return f'''
# <!doctype html>
# <html>
#     <body>
#         <h1>Добавлен новый цветок</h1>
#         <p>Название нового цветка: {name} </p>
#         <p>Всего цветов: {len(flower_list)} </p>
#         <p>Полный список: {flower_list} </p>
#     </body>
# </html> '''

# @lab2.route('/lab2/all_flowers') #вывод всех цветов
# def all_flowers():
#     flower_items = ''.join([f'<li>{i}. {flower}</li>' for i, flower in enumerate(flower_list)]) # Функция enumerate() пробегает по списку и даёт одновременно индекс и значение каждого элемента. Метод join() склеивает все элементы списка в одну большую строку без разделителей
#     return f'''
# <!doctype html>
# <html>
#     <body>
#         <h1>Все цветы</h1>
#         <ul>
#             {flower_items}
#         </ul>
#         <p>Всего: {len(flower_list)}</p>
#     </body>
# </html>'''


# @lab2.route('/lab2/clear_flowers') # очищение списка цветов
# def clear_flowers():
#     flower_list.clear()
#     return '''
# <!doctype html>
# <html>
#     <body>
#         <h1>Список цветов очищен!</h1>
#         <a href="/lab2/all_flowers">Посмотреть список</a>
#     </body>
# </html>
# '''


@lab2.route('/lab2/example')
def example():
    name, group, course, lab = 'Софья Анчугова', 'ФБИ-32', '3 курс', '2'
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'aпельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    return render_template('lab2/example.html', name=name, group=group, course=course, lab=lab, fruits=fruits) # параметры шаблона 

@lab2.route('/lab2/') 
def lab():
    return render_template('lab2/lab2.html')


@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('lab2/filter.html', phrase = phrase)



@lab2.route('/lab2/calc/<int:a>/<int:b>')
def lab2_calc(a, b):
    # Чтобы избежать деления на ноль:
    if b == 0:
        div_result = 'нельзя делить на 0'
    else:
        div_result = a / b

    return f'''
<!doctype html>
<html>
    <body>
        <h1>Расчёт с параметрами:</h1>
        <p>{a} + {b} = {a + b}</p>
        <p>{a} - {b} = {a - b}</p>
        <p>{a} * {b} = {a * b}</p>
        <p>{a} / {b} = {div_result}</p>
        <p>{a}<sup>{b}</sup> = {a ** b}</p>
    </body>
</html>
'''

@lab2.route('/lab2/calc/') # перекидывает на адрес с 1/1
def calc_default():
    return redirect('/lab2/calc/1/1')

@lab2.route('/lab2/calc/<int:a>') # перекидывает на адрес с a/1
def calc_single(a):
    return redirect(f'/lab2/calc/{a}/1')



@lab2.route('/lab2/books')
def books():
    book_list = [
        {"title": "Мастер и Маргарита", "author": "Михаил Булгаков", "genre": "Роман", "pages": 480},
        {"title": "Преступление и наказание", "author": "Фёдор Достоевский", "genre": "Роман", "pages": 672},
        {"title": "Война и мир", "author": "Лев Толстой", "genre": "Роман-эпопея", "pages": 1225},
        {"title": "Евгений Онегин", "author": "Александр Пушкин", "genre": "Роман в стихах", "pages": 384},
        {"title": "Герой нашего времени", "author": "Михаил Лермонтов", "genre": "Роман", "pages": 320},
        {"title": "Анна Каренина", "author": "Лев Толстой", "genre": "Роман", "pages": 864},
        {"title": "Двенадцать стульев", "author": "Ильф и Петров", "genre": "Сатирический роман", "pages": 400},
        {"title": "Собачье сердце", "author": "Михаил Булгаков", "genre": "Повесть", "pages": 200},
        {"title": "Чевенгур", "author": "Андрей Платонов", "genre": "Роман", "pages": 480},
        {"title": "Тихий Дон", "author": "Михаил Шолохов", "genre": "Роман", "pages": 960}
    ]
    return render_template('lab2/books.html', books=book_list)



@lab2.route('/lab2/cats')
def cats():
    cats = [
        {"name": "Барсик", "image": "cats/кот 1.jpg", "desc": "Милый пушистый кот, любит спать на подоконнике."},
        {"name": "Мурка", "image": "cats/кот 2.jpg", "desc": "Ласковая кошка с зелёными глазами."},
        {"name": "Симба", "image": "cats/кот 3.jpg", "desc": "Отважный котёнок, который считает себя львом."},
        {"name": "Пушок", "image": "cats/кот 4.jpg", "desc": "Белый как снег, любит играть с клубком ниток."},
        {"name": "Том", "image": "cats/кот 5.jpg", "desc": "Хитрый кот, охотится за мышами."},
        {"name": "Луна", "image": "cats/кот 6.jpg", "desc": "Ночная хищница с блестящей шерстью."},
        {"name": "Гарфилд", "image": "cats/кот 7.jpg", "desc": "Любит лазанью и сон."},
        {"name": "Честер", "image": "cats/кот 8.jpg", "desc": "Энергичный рыжий кот, обожает прыгать."},
        {"name": "Милка", "image": "cats/кот 9.jpg", "desc": "Пятнистая кошечка, напоминает корову."},
        {"name": "Феликс", "image": "cats/кот 10.jpg", "desc": "Настоящий джентльмен среди котов."},
        {"name": "Соня", "image": "cats/кот 11.jpg", "desc": "Очень спокойная, любит дремать по 18 часов в день."},
        {"name": "Мотя", "image": "cats/кот 12.jpg", "desc": "Озорной котёнок, не сидит на месте."},
        {"name": "Буся", "image": "cats/кот 13.jpg", "desc": "Сладко мурлычет, когда её гладят."},
        {"name": "Бакс", "image": "cats/кот 14.jpg", "desc": "Пушистый и важный, любит смотреть на птиц."},
        {"name": "Карамелька", "image": "cats/кот 15.jpg", "desc": "Маленькая и шустрая, как кусочек сахара."},
        {"name": "Черныш", "image": "cats/кот 16.jpg", "desc": "Чёрный кот, но приносит только удачу."},
        {"name": "Мурзик", "image": "cats/кот 17.jpg", "desc": "Любопытный и смешной котик."},
        {"name": "Тигра", "image": "cats/кот 18.jpg", "desc": "Кошка-охотница с тигровыми полосками."},
        {"name": "Рыжик", "image": "cats/кот 19.jpg", "desc": "Самый рыжий из всех котов."},
        {"name": "Лео", "image": "cats/кот 20.jpg", "desc": "Грациозный кот с королевскими манерами."}
    ]
    return render_template('lab2/cats.html', cats=cats)



flower_list = [
    {"name": "роза", "price": 300},
    {"name": "тюльпан", "price": 310},
    {"name": "незабудка", "price": 320},
    {"name": "ромашка", "price": 330},
    {"name": "георгин", "price": 300},
    {"name": "гладиолус", "price": 310}
]

@lab2.route('/lab2/flowers/') # открываем страницу flowers.html, подтягиваем туда словарь в цветами flower_list в часетве переменной flowers (она используется в flowers.html)
def show_flowers():
    return render_template('lab2/flowers.html', flowers=flower_list)

@lab2.route('/lab2/add_flower', methods=['POST']) # Flask ждёт, что запрос будет не обычным GET (через адресную строку), а POST (через форму)
def add_flower():
    name = request.form.get('name') # забирают значения, введённые пользователем в поля формы <input name="name"> и <input name="price">.
    price = request.form.get('price')

    if not name or not price: # сервер возвращает ошибку если хотбы одно не заполнено
        abort(400)

    flower_list.append({"name": name, "price": int(price)}) # В конец списка flower_list добавляется новый словарь (объект цветка), int(price) — приводит цену к целому числу (чтобы с ней можно было потом работать как с числом)
    return redirect(url_for('lab2.show_flowers')) # После добавления цветка пользователя перенаправляют обратно на страницу со всеми цветами

@lab2.route('/lab2/del_flower/<int:flower_id>') # <int:flower_id> - выбираем цветок по индексу  
def del_flower(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list): # если индекс меньше 0 или больше, чем длина списка — такой цветок не существует, выдаётся ошибка 404 Not Found.
        abort(404)
    del flower_list[flower_id] # удаляет цветок из списка по индексу.
    return redirect(url_for('lab2.show_flowers')) # перенаправление обратно на страницу со списком

@lab2.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear() # очищает список полностью
    return redirect(url_for('lab2.show_flowers')) # перенаправление обратно на страницу со списком чтобы обновить вид сразу

