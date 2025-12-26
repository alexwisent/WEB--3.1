from flask import Blueprint, render_template, request, redirect, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from db.models import users, articles
from sqlalchemy import or_, func

# Создаем Blueprint для раздела "lab8"
lab8 = Blueprint('lab8', __name__)


@lab8.route('/lab8/')   # Главная страница лабораторной работы
def lab():
    # Если пользователь авторизован, используем его логин, иначе "Anonymous"
    if current_user.is_authenticated:   
        login = current_user.login
    else:
        login = 'Anonymous'
    # Отправляем логин в шаблон
    return render_template('lab8/lab8.html', login=login)


@lab8.route('/lab8/register/', methods=['GET', 'POST'])     # Регистрация нового пользователя
def register():
    if request.method == 'GET':
        # Отображаем форму регистрации
        return render_template('lab8/register.html')
    
    # Получаем данные из формы
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    
    # Проверка пустых полей
    if not login_form or login_form.strip() == '':
        return render_template('lab8/register.html',
                            error='Имя пользователя не может быть пустым')
    
    if not password_form or password_form.strip() == '':
        return render_template('lab8/register.html',
                            error='Пароль не может быть пустым')
    
    # Проверяем, существует ли уже пользователь с таким логином
    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html',
                            error='Такой пользователь уже существует')

    # Хэшируем пароль и создаем нового пользователя
    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    
    # Логиним нового пользователя
    login_user(new_user, remember=False)
    
    # Перенаправляем на главную страницу lab8
    return redirect('/lab8/')


@lab8.route('/lab8/login/', methods=['GET', 'POST'])    # Вход пользователя
def login():
    if request.method == 'GET':
        # Отображаем форму входа
        return render_template('lab8/login.html')
    
    # Получаем данные из формы
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember_me = request.form.get('remember') == 'on'  # галочка "запомнить меня"
    
    # Проверка пустых полей
    if not login_form or login_form.strip() == '':
        return render_template('lab8/login.html',
                            error='Логин не может быть пустым')
    
    if not password_form or password_form.strip() == '':
        return render_template('lab8/login.html',
                            error='Пароль не может быть пустым')
    
    # Ищем пользователя в базе данных
    user = users.query.filter_by(login=login_form).first()

    # Проверяем пароль и логиним пользователя
    if user and check_password_hash(user.password, password_form):
        login_user(user, remember=remember_me)
        return redirect('/lab8/')

    # Ошибка при неверном логине или пароле
    return render_template('lab8/login.html',
                        error='Ошибка входа: логин и/или пароль неверны')


@lab8.route('/lab8/articles/')      # Просмотр своих статей (только для авторизованных)
@login_required
def article_list():
    # Получаем все статьи текущего пользователя
    user_articles = articles.query.filter_by(
        login_id=current_user.id
    ).all()

    # Передаем статьи в шаблон
    return render_template(
        'lab8/articles.html',
        articles=user_articles
    )


@lab8.route('/lab8/logout/')    # Выход пользователя
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')


@lab8.route('/lab8/create/', methods=['GET', 'POST'])   # Создание новой статьи
@login_required
def create():
    if request.method == 'GET':
        # Отображаем форму создания статьи
        return render_template('lab8/create.html')

    # Получаем данные из формы
    title = request.form.get('title')
    text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'on'

    # Проверка обязательных полей
    if not title or not text:
        return render_template(
            'lab8/create.html',
            error='Заголовок и текст статьи обязательны'
        )

    # Создаем новую статью
    new_article = articles(
        login_id=current_user.id,
        title=title,
        article_text=text,
        is_public=is_public
    )

    db.session.add(new_article)
    db.session.commit()

    return redirect('/lab8/articles/')


@lab8.route('/lab8/edit/<int:article_id>/', methods=['GET', 'POST'])    # Редактирование существующей статьи
@login_required
def edit(article_id):
    # Получаем статью по id и текущему пользователю
    article = articles.query.filter_by(
        id=article_id,
        login_id=current_user.id
    ).first_or_404()

    if request.method == 'GET':
        # Отображаем форму редактирования статьи
        return render_template('lab8/edit.html', article=article)

    # Обновляем поля статьи
    article.title = request.form.get('title')
    article.article_text = request.form.get('article_text')
    article.is_public = request.form.get('is_public') == 'on'

    db.session.commit()
    return redirect('/lab8/articles/')


@lab8.route('/lab8/delete/<int:article_id>/')   # Удаление статьи
@login_required
def delete(article_id):
    # Получаем статью по id и текущему пользователю
    article = articles.query.filter_by(
        id=article_id,
        login_id=current_user.id
    ).first_or_404()

    # Удаляем статью
    db.session.delete(article)
    db.session.commit()

    return redirect('/lab8/articles/')


@lab8.route('/lab8/public/')    # Просмотр публичных статей (доступно всем)
def public_articles():
    public_articles = (
        articles.query
        .filter_by(is_public=True)
        .join(users)  # соединяем с таблицей пользователей, чтобы иметь доступ к информации о авторе
        .all()
    )

    return render_template(
        'lab8/public.html',
        articles=public_articles
    )


@lab8.route('/lab8/articles/search/', methods=['GET'])  # Поиск по своим статьям (авторизованный пользователь)
@login_required
def search_articles():
    query = request.args.get('q', '').strip()
    if query:
        q_lower = query.lower()
        # Фильтруем статьи текущего пользователя по заголовку или тексту
        user_articles = articles.query.filter(
            articles.login_id == current_user.id,
            or_(
                func.lower(articles.title).like(f"%{q_lower}%"),
                func.lower(articles.article_text).like(f"%{q_lower}%")
            )
        ).all()
    else:
        # Если запрос пустой, возвращаем все статьи пользователя
        user_articles = articles.query.filter_by(login_id=current_user.id).all()

    return render_template('lab8/articles.html', articles=user_articles, search_query=query)


@lab8.route('/lab8/public/search/', methods=['GET'])    # Поиск по публичным статьям (для всех)
def search_public_articles():
    query = request.args.get('q', '').strip()
    if query:
        q_lower = query.lower()
        # Фильтруем публичные статьи по заголовку или тексту
        public_articles = articles.query.filter(
            articles.is_public == True,
            or_(
                func.lower(articles.title).like(f"%{q_lower}%"),
                func.lower(articles.article_text).like(f"%{q_lower}%")
            )
        ).join(users).all()
    else:
        public_articles = articles.query.filter_by(is_public=True).join(users).all()

    return render_template('lab8/public.html', articles=public_articles, search_query=query)
