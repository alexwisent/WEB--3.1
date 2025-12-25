from flask import Blueprint, render_template, request, jsonify, session
from flask_login import current_user, login_required
from db import db
from db.models import gifts
import random

lab9 = Blueprint('lab9', __name__)

BOXES_COUNT = 10
MAX_OPENED = 3
GIFTS = [
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

def init_gifts():
    if gifts.query.count() == 0:
        positions = [(random.randint(50, 900), random.randint(50, 400)) for _ in range(BOXES_COUNT)]
        box_numbers = list(range(1, BOXES_COUNT + 1))
        random.shuffle(box_numbers)
        for i, box_number in enumerate(box_numbers):
            gift = GIFTS[i]
            g = gifts(
                box_number=box_number,
                message=gift['message'],
                image=gift['image'],
                pos_x=positions[i][0],
                pos_y=positions[i][1]
            )
            db.session.add(g)
        db.session.commit()

@lab9.route('/lab9/')
def main():
    init_gifts()
    boxes = gifts.query.order_by(gifts.box_number).all()
    
    if current_user.is_authenticated:
        opened_count = gifts.query.filter_by(opened_by=current_user.id).count()
    else:
        if 'opened_count' not in session:
            session['opened_count'] = 0
        opened_count = session['opened_count']
    
    remaining = MAX_OPENED - opened_count
    return render_template('lab9/index.html',
                           boxes=boxes,
                           remaining=remaining,
                           opened_count=opened_count,
                           max_opened=MAX_OPENED,
                           boxes_count=BOXES_COUNT,
                           login=current_user.is_authenticated)

@lab9.route('/lab9/open/', methods=['POST'])
def open_box():
    box_id = request.json.get('box_id')
    
    if current_user.is_authenticated:
        opened_count = gifts.query.filter_by(opened_by=current_user.id).count()
    else:
        if 'opened_count' not in session:
            session['opened_count'] = 0
        opened_count = session['opened_count']
    
    if opened_count >= MAX_OPENED:
        return jsonify({'error': f'Вы уже открыли {MAX_OPENED} коробки!'}), 400

    box = gifts.query.get(box_id)
    if not box:
        return jsonify({'error': 'Коробка не найдена'}), 404
    
    if current_user.is_authenticated:
        if box.opened_by is not None:
            return jsonify({'error': 'Коробка уже открыта'}), 400
        box.opened_by = current_user.id
    else:
        if 'guest_opened' not in session:
            session['guest_opened'] = []
        if box.id in session['guest_opened']:
            return jsonify({'error': 'Коробка уже открыта'}), 400
        session['guest_opened'].append(box.id)
        session['opened_count'] = session.get('opened_count', 0) + 1
        session.modified = True

    db.session.commit()

    return jsonify({
        'message': box.message,
        'image': box.image,
        'remaining': MAX_OPENED - (opened_count + 1)
    })

@lab9.route('/lab9/magic/', methods=['POST'])
@login_required
def magic():
    user_boxes = gifts.query.filter_by(opened_by=current_user.id).all()
    for box in user_boxes:
        box.opened_by = None
    db.session.commit()
    return jsonify({'status': 'ok'})
