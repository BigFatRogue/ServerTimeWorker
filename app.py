from sitting import *
import git

from flask import Flask, request, jsonify, render_template, url_for, session, flash, redirect
from flask_session import Session
from flask_cors import CORS

from authentication import registration_user
from get_users_json import get_user_calendar_json, update_calendar_user_json
from db import *


app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(SESSION_COOKIE_SAMESITE=SESSION_COOKIE_SAMESITE, SESSION_COOKIE_SECURE=SESSION_COOKIE_SECURE)
Session(app)
CORS(app, supports_credentials=SUPPORTS_CREDENTIALS)


@app.route("/")
def index():
    print(session)
    if session.get('userLogged'):
        return redirect(url_for('calendar'))
    return redirect(url_for('authentication'))


@app.route("/registration", methods=["POST"])
def registration():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        repet_password = request.form.get('repet-password')

        if password == repet_password:
            flag, msg = registration_user(username, password)
            if not flag:
                flash(msg, category='error')
            flash(msg, category='success')
        else:
            flash("Пароли на совпадают", category='error')
    return render_template('authentication.html')


@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        db = UsersDB()
        flag, user_id, data = db.get_users(username, password)

        if flag:
            if not session.get('userLogged'):
                session['userLogged'] = {'id': user_id}
            return redirect(url_for('calendar'))
        else:
            flash(data, category='error')
    return render_template('authentication.html')


@app.route("/calendar")
def calendar():
    if session.get('userLogged'):
        user_id = session.get('userLogged').get('id')
        return render_template('calendar.html', user_id=user_id)
    return 'УПС'


@app.route("/authentication")
def authentication():
    return render_template('authentication.html')


@app.route("/logout", methods=["POST"])
def logout():
    if request.method == "POST":
        session.clear()
        return redirect(url_for('authentication'))


@app.route("/get_calendar/<user_id>")
def get_calendar(user_id):
    return jsonify(get_user_calendar_json(user_id=user_id))


@app.route("/session_reboot")
def session_reboot():
    session.clear()
    return 'Сессия очищена'


@app.route("/update_calendar_user", methods=["POST"])
def update_calendar_user():
    if request.method == "POST":
        data: dict = eval(request.data)
        if update_calendar_user_json(data):
            return jsonify({'status': 'success'})
        return jsonify({'status': 'error'})


@app.route("/update_server", methods=["POST"])
def webhook():
    if request.method == "POST":
        repo = git.Repo('')
        origin = repo.remotes.origin

        origin.pull()
        return 'Update PythonAnywhere successfully', 200
    else:
        return 'Wrong event type 1', 400


@app.after_request
def add_security_headers(resp):
    resp.headers['Content-Security-Policy'] = 'frame-src http://127.0.0.1:5000/'
    return resp


if __name__ == '__main__':
    app.run()
