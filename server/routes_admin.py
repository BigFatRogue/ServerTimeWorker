import os.path

from flask import render_template, redirect, url_for, request, flash, jsonify, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from server import app
from server.database.db import Admin, Users, load_zipdb, upload_zipdb
from server.database.UserLogin import UserLogin
from server.my_sitting import PROJECT_ROOT


@app.route("/admin")
def admin():
    if current_user.is_authenticated:
        return redirect(url_for('admin_panel'))
    return render_template('admin_panel/admin_login.html')


@app.route("/admin-login", methods=['POST'])
def admin_login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        db = Admin()
        flag, user_db = db.get_set_admin(username, generate_password_hash(password))

        if flag:
            if check_password_hash(user_db[-1], password):
                login_user(UserLogin().create(user_db), remember=True)
                return redirect(url_for('admin_panel'))
            else:
                flash('Неверный пароль', 'log-error')
                return render_template('admin_panel/admin_login.html')
    return redirect(url_for('admin'))


@app.route("/admin-logout", methods=["GET", "POST"])
def admin_logout():
    logout_user()
    return redirect(url_for('authentication'))


@app.route("/admin-panel")
@login_required
def admin_panel():
    if current_user.get_id() == '1000':
        db = Users()
        data = db.get_all_users()
        return render_template('admin_panel/admin_panel.html', users=data['users'], column=data['column'])
    return redirect('/')


@app.route("/update_user_name", methods=['POST'])
@login_required
def update_user_name():
    if request.method == 'POST':
        data = eval(request.data)
        db_users = Users()
        user_id = str(data['user_id']).strip()
        username = str(data['username']).strip()
        password = str(data['password']).strip()

        if username:
            db_users.update_username(user_id, username)
        if password or password != '***':
            db_users.update_password(user_id, password)

    return jsonify({'status_update_user': 'success'})


@app.route("/del_user", methods=['POST'])
@login_required
def del_user():
    if request.method == 'POST':
        data = eval(request.data)
        db_users = Users()
        user_id = str(data['user_id']).strip()
        db_users.del_user(user_id)
    return jsonify({'status_del_user': 'success'})


@app.route("/del_admin", methods=['GET', 'POST'])
@login_required
def del_admin():
    db = Admin()
    db.del_admin()
    logout_user()
    return redirect('/')


@app.route("/load_db", methods=['GET', 'POST'])
@login_required
def load_db():
    # Загрузка db.db и папки users с сервера
    zipname = load_zipdb()
    print(zipname)
    return send_from_directory(PROJECT_ROOT, zipname)


@app.route("/upload_db", methods=['POST'])
@login_required
def upload_db():
    # Загрузка db.db и папки users на сервера
    if request.method == 'POST':
        file = request.files['file']
        if file and '.zip' in file.filename:
            if os.path.exists(os.path.join(PROJECT_ROOT, 'database_upload.zip')):
                os.remove(os.path.join(PROJECT_ROOT, 'database_upload.zip'))

            file.save(os.path.join(PROJECT_ROOT, 'database_upload.zip'))
            upload_zipdb()
            return redirect(url_for('admin'))
    return redirect(url_for('admin'))

@app.route("/upload-calendar", methods=['POST'])
@login_required
def upload_calendar():
    # Загрузка календарь на год и обновить у всех пользователей
    if request.method == 'POST':
        file = request.files['file']
        if file:
            pass
    return redirect(url_for('admin'))