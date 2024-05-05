from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from server import app
from server.database.db import Admin, Users
from server.database.UserLogin import UserLogin


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
    return redirect(url_for('admin'))

