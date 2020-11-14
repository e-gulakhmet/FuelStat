# Данные файл содержит в себе функции для отображения страниц, по
# указанным путям


from app import flsk
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user
from app.models import User



@flsk.route("/index")
def index():
    return render_template("index.html", title="Index", user=current_user)



@flsk.route("/", methods=["GET", "POST"])
@flsk.route("/login", methods=["GET", "POST"])
def login():
    # При входе на сайт, пользователь сразу переходит к странице
    # авторизации.
    # Он вводит свой логин и пароль, а так как пользователь у нас один,
    # то проверяем введенные данные с данными, которые у нас есть.
    # Если были введены верные данные, то переводим его на основную
    # страницу.
    # Иначе просим его ввести данные снова.

    user = User("admin", "admin")

    # Проверяем, если пользователь уже зашел,
    # то отправляем его на основную страницу.
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # Создаем объект form, который содержит в себе веб-формы для
    # авторизации
    form = LoginForm()
    # Если пришел POST запрос от браузера
    if form.validate_on_submit():
        if user.username != form.username.data:
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # Иначе загружаем пользователя
        # и переходим к основной странице
        login_user(user, remember=True)
        return redirect(url_for("index"))
    # Генерируем страницу авторизиции
    return render_template('login.html', title='Login', form=form)



@flsk.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))