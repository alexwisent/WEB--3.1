from flask import Blueprint, render_template
from flask_login import current_user

rgz = Blueprint('rgz', __name__)

@rgz.route('/rgz/')
def main():
    if current_user.is_authenticated:
        login = current_user.login
    else:
        login = 'Гость'
    return render_template('rgz/rgz.html', login=login)
