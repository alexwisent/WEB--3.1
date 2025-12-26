from flask import Blueprint, render_template, request, jsonify, session
from flask_login import current_user, login_required
from db import db
from db.models import gifts
import random

lab9 = Blueprint('lab9', __name__) 	# Создаем Blueprint для модуля lab9

BOXES_COUNT = 10 	# Количество коробок
MAX_OPENED = 3 	# Максимальное количество коробок, которые можно открыть
GIFTS = [ 	# Список подарков с сообщением и изображением
    {'message': 'С Новым Годом!', 'image': 'gifts/k1.jpg'},
    {'message': 'Удачи в новом году!', 'image': 'gifts/k2.jpg'},
    {'message': 'Пусть сбудутся мечты!', 'image': 'gifts/k3.jpg'},
    {'message': 'Счастья и здоровья!', 'image': 'gifts/k4.jpg'},
    {'message': 'Веселых праздников!', 'image': 'gifts/k5.jpg'},
    {'message': 'Мира и добра!', 'image': 'gifts/k6.jpg'},
    {'message': 'Сюрприз внутри!', 'image': 'gifts/k7.jpg'},
    {'message': 'Подарок для тебя!', 'image': 'gifts/k8.jpg'},
    {'message': 'Сказочного настроения!', 'image': 'gifts/k9.jpg'},
    {'message': 'Радости и улыбок!', 'image': 'gifts/k10.jpg'},
]

def init_gifts(): 	# Инициализация подарков в базе данных
    if gifts.query.count() == 0: 	# Если таблица подарков пуста
        positions = [(random.randint(50, 900), random.randint(50, 400)) for _ in range(BOXES_COUNT)] 	# Генерация случайных координат для коробок
        box_numbers = list(range(1, BOXES_COUNT + 1)) 	# Создаем список номеров коробок
        random.shuffle(box_numbers) 	# Перемешиваем номера коробок
        for i, box_number in enumerate(box_numbers): 	# Создаем объекты подарков
            gift = GIFTS[i]
            g = gifts(
                box_number=box_number, 	# Номер коробки
                message=gift['message'], 	# Сообщение подарка
                image=gift['image'], 	# Изображение подарка
                pos_x=positions[i][0], 	# Координата X
                pos_y=positions[i][1] 	# Координата Y
            )
            db.session.add(g) 	# Добавляем подарок в сессию базы данных
        db.session.commit() 	# Сохраняем изменения в базе данных

@lab9.route('/lab9/')
def main(): 	# Главная страница модуля
    init_gifts() 	# Инициализация подарков
    boxes = gifts.query.order_by(gifts.box_number).all() 	# Получаем все коробки из базы, сортируя по номеру
    
    if current_user.is_authenticated: 	# Если пользователь вошел в систему
        opened_count = gifts.query.filter_by(opened_by=current_user.id).count() 	# Считаем количество открытых им коробок
    else:
        if 'opened_count' not in session: 	# Если пользователь гость и счетчик не установлен
            session['opened_count'] = 0 	# Инициализируем счетчик
        opened_count = session['opened_count'] 	# Получаем текущее количество открытых коробок

    remaining = MAX_OPENED - opened_count 	# Вычисляем оставшееся количество коробок, которые можно открыть
    return render_template('lab9/index.html',
                           boxes=boxes,
                           remaining=remaining,
                           opened_count=opened_count,
                           max_opened=MAX_OPENED,
                           boxes_count=BOXES_COUNT,
                           login=current_user.is_authenticated) 	# Передаем данные в шаблон

@lab9.route('/lab9/open/', methods=['POST'])
def open_box(): 	# Открытие коробки
    box_id = request.json.get('box_id') 	# Получаем ID коробки из запроса
    
    if current_user.is_authenticated: 	# Если пользователь вошел в систему
        opened_count = gifts.query.filter_by(opened_by=current_user.id).count() 	# Считаем количество открытых коробок
    else:
        if 'opened_count' not in session: 	# Если пользователь гость и счетчик не установлен
            session['opened_count'] = 0
        opened_count = session['opened_count'] 	# Получаем текущее количество открытых коробок
    
    if opened_count >= MAX_OPENED: 	# Проверяем лимит открытых коробок
        return jsonify({'error': f'Вы уже открыли {MAX_OPENED} коробки!'}), 400

    box = gifts.query.get(box_id) 	# Получаем коробку по ID
    if not box:
        return jsonify({'error': 'Коробка не найдена'}), 404 	# Если коробка не найдена

    if current_user.is_authenticated: 	# Для зарегистрированного пользователя
        if box.opened_by is not None: 	# Проверяем, открыта ли уже коробка
            return jsonify({'error': 'Коробка уже открыта'}), 400
        box.opened_by = current_user.id 	# Присваиваем коробке пользователя, который открыл
    else: 	# Для гостя
        if 'guest_opened' not in session:
            session['guest_opened'] = [] 	# Список открытых коробок гостя
        if box.id in session['guest_opened']: 	# Проверяем, не открыта ли коробка
            return jsonify({'error': 'Коробка уже открыта'}), 400
        session['guest_opened'].append(box.id) 	# Добавляем коробку в список открытых
        session['opened_count'] = session.get('opened_count', 0) + 1 	# Увеличиваем счетчик открытых коробок
        session.modified = True 	# Отмечаем сессию как измененную

    db.session.commit() 	# Сохраняем изменения в базе данных

    return jsonify({
        'message': box.message, 	# Сообщение из коробки
        'image': box.image, 	# Изображение из коробки
        'remaining': MAX_OPENED - (opened_count + 1) 	# Количество оставшихся коробок
    })

@lab9.route('/lab9/magic/', methods=['POST'])
@login_required 	# Доступно только авторизованным пользователям
def magic(): 	# "Волшебная" функция сброса открытых коробок
    user_boxes = gifts.query.filter_by(opened_by=current_user.id).all() 	# Получаем все коробки, открытые пользователем
    for box in user_boxes:
        box.opened_by = None 	# Сбрасываем информацию об открытии
    db.session.commit() 	# Сохраняем изменения
    return jsonify({'status': 'ok'}) 	# Возвращаем статус успешного сброса
