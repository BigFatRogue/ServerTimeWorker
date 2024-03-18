import git
from my_sitting import DATABASE, SECRET_KEY, SESSION_TYPE, DEBUG, THREADED, SESSION_COOKIE_SAMESITE, SESSION_COOKIE_SECURE, SUPPORTS_CREDENTIALS
from flask import Flask, request, jsonify, render_template, url_for, session, flash, redirect
from flask_session import Session
from flask_cors import CORS

from get_users_json import get_user_calendar_json, update_calendar_user_json
from my_db import UsersDB


app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(SESSION_COOKIE_SAMESITE=app.config['SESSION_COOKIE_SAMESITE'], SESSION_COOKIE_SECURE=app.config['SESSION_COOKIE_SECURE'] )
Session(app)
CORS(app, supports_credentials=app.config['SUPPORTS_CREDENTIALS'])


@app.route("/")
def index():
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
            db = UsersDB()
            flag, msg = db.set_users(username, password)
            if not flag:
                flash(msg, category='reg-error')
            else:
                flash(msg, category='reg-success')
        else:
            flash("Пароли на совпадают", category='reg-error')
    return render_template('authentication.html', page='reg')


@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        db = UsersDB()
        flag, user_id, data = db.get_user(username, password)

        if flag:
            if not session.get('userLogged'):
                session['userLogged'] = {'id': user_id, 'username': username}
            return redirect(url_for('calendar'))
        else:
            flash(data, category='log-error')
    return render_template('authentication.html', page='auth')
    # return redirect(url_for('authentication'))


@app.route("/calendar")
def calendar():
    if session.get('userLogged'):
        user_id = session.get('userLogged').get('id')
        username = session.get('userLogged').get('username')
        return render_template('calendar.html', user_id=user_id, username=username)
    return 'УПС'


@app.route("/authentication")
def authentication():
    return render_template('authentication.html', page='auth')


@app.route("/logout", methods=["POST"])
def logout():
    if request.method == "POST":
        session.clear()
        return redirect(url_for('authentication'))


@app.route("/get_calendar/<user_id>")
def get_calendar(user_id):
    print(user_id)
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
    resp.headers['Content-Security-Policy'] = 'frame-src https://catlulyk.pythonanywhere.com'
    return resp


if __name__ == '__main__':
    app.run()
