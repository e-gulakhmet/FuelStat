from app import flsk
from flask import render_template
from app.forms import LoginForm


@flsk.route('/')
@flsk.route('/login')
def login():
    # При входе на сайт, пользователя сразу переходит к странице
    # авторизации.
    # Он вводит свой логин и пароль, а так как пользователь у нас один,
    # то проверяем введенные данные с данными, которые у нас есть.
    # Если были введены верные данные, то переводим его на основную
    # страницу.
    # Иначе просим его ввести данные снова. 
    user = {"name": "operator", "password": "operator"}
    form = LoginForm()
    return render_template('login.html', title='Login', user=user, form=form)
