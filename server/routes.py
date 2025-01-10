from flask import request, render_template, url_for, flash, redirect, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required
import git
from werkzeug.security import generate_password_hash, check_password_hash

from server import app, login_manager
from server.database.get_users_json import get_user_calendar_json, update_calendar_user_json, get_users_time_bitrix, write_data_bitrix_user, check_user_bitrix_data, create_standart_calendar
from server.database.db import Users, Admin
from server.database.UserLogin import UserLogin


@login_manager.user_loader
def load_user(user_id):
    if 'admin' in request.url:
        return UserLogin().from_db(user_id, Admin())
    return UserLogin().from_db(user_id, Users())


@app.route("/")
def index():
    if current_user.is_authenticated:
        user_id = current_user.get_id()
        username = current_user.get_username()

        if check_user_bitrix_data(user_id):
            return redirect(url_for('calendar'))
        else:
            return render_template('auth/authentication_data_bitrix.html', user_id=user_id, username=username)
    return redirect(url_for('authentication'))


@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        db = Users()
        flag, user_db = db.get_user_username(username)

        if flag:
            user_id, username_db, password_db, filepath_db = user_db
            if not check_password_hash(password_db, password):
                flash('Неверный пароль', category='log-error')
                return render_template('auth/authentication_user.html', page='auth')

            login_user(UserLogin().create(user_db), remember=True)
            if check_user_bitrix_data(user_id):
                return redirect(url_for('calendar'))
            else:
                return render_template('auth/authentication_data_bitrix.html', user_id=user_id, username=username)
        else:
            flash('Неверное имя пользователя', category='log-error')
    return render_template('auth/authentication_user.html', page='auth')


@app.route("/registration", methods=["POST"])
def registration():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        repet_password = request.form.get('repet-password')

        if password == repet_password:
            db = Users()
            flag, user_id = db.set_users(username, generate_password_hash(password))
            if flag:
                return render_template('auth/authentication_data_bitrix.html', user_id=user_id, username=username)
            else:
                flash('Такой пользователь уже существует', category='reg-error')
                
        else:
            flash("Пароли на совпадают", category='reg-error')
    return render_template('auth/authentication_user.html', page='reg')


@app.route("/calendar")
@login_required
def calendar():
    user_id = current_user.get_id()
    username = current_user.get_username()
    return render_template('calendar/calendar.html', user_id=user_id, username=username)


@app.route("/authentication")
def authentication():
    return render_template('auth/authentication_user.html', page='auth')


@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for('authentication'))


@app.route("/page-update-data-bitrix", methods=["GET", "POST"])
def page_update_data_bitrix():
    return render_template('calendar/page_update_data_bitrix.html', user_id=current_user.get_id())


@app.route("/update-data-bitrix", methods=["POST"])
def update_data_bitrix():
    if request.method == 'POST':
        data = request.form.get('bush-cod')
        user_id = request.form.get('user_id')
    
        res = write_data_bitrix_user(user_id=user_id, string=data)
        if not res:
            flash(message='Неверно скопированный bush код', category='error')
            return render_template('calendar/page_update_data_bitrix.html', user_id=user_id)
        flash(f'Bush код обновлён', category='log-success')

        return render_template('calendar/page_update_data_bitrix.html', user_id=user_id)
    

@app.route("/get_calendar/<user_id>")
@login_required
def get_calendar(user_id):
    return jsonify(get_user_calendar_json(user_id=user_id))


@app.route("/get_my_hours", methods=["POST"])
@login_required
def get_my_hours():
    if request.method == "POST":
        data: dict = eval(request.data)
        return jsonify(get_users_time_bitrix(**data))


@app.route("/update_calendar_user", methods=["POST"])
@login_required
def update_calendar_user():
    if request.method == "POST":
        data: dict = eval(request.data)

        if update_calendar_user_json(data):
            return jsonify({'status': 'success'})
        return jsonify({'status': 'error'})


@app.route("/set_data_bitrix", methods=["POST"])
def set_data_bitrix():
    if request.method == "POST":
        data = request.form.get('bush-cod')
        user_id = request.form.get('user_id')
        username = request.form.get('username')

        res = write_data_bitrix_user(user_id=user_id, string=data)
        if not res:
            flash(message='Неверно скопированный bush код', category='error')
            return render_template('auth/authentication_data_bitrix.html', user_id=user_id)
        flash(f'Новый пользователь {username} зарегистрирован', category='log-success')

        db = Users()
        flag, user_db = db.get_user_username(username)
        login_user(UserLogin().create(user_db), remember=True)

        return redirect(url_for('calendar'))


@app.route("/instruction")
def instruction():
    return render_template('auth/instruction.html')


