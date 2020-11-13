# Данные файл содержит в себе функции для отображения страниц, по
# указанным путям


from app import flsk
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm

user = {"username": "operator", "password": "operator"}


@flsk.route("/")
@flsk.route("/index")
def index():
    return render_template("index.html", title="Index", user=user)


@flsk.route("/login", methods=["GET", "POST"])
def login():
    # При входе на сайт, пользователь сразу переходит к странице
    # авторизации.
    # Он вводит свой логин и пароль, а так как пользователь у нас один,
    # то проверяем введенные данные с данными, которые у нас есть.
    # Если были введены верные данные, то переводим его на основную
    # страницу.
    # Иначе просим его ввести данные снова.

    # Создаем объект form, который содержит в себе веб-формы для
    # авторизации
    form = LoginForm()
    # Если пришел POST запрос от браузера
    if form.validate_on_submit():
        # Говорим, какой логин был получен
        flash("Login requested for user {}".format(
            form.username.data))
        # Переходим к другой странице
        return redirect(url_for("index"))
    # Генерируем страницу авторизиции
    return render_template('login.html', title='Login', user=user, form=form)
