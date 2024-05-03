from server.my_sitting import *
from flask import Flask
from flask_login import LoginManager, logout_user, login_user
# from flask_session import Session
from flask_cors import CORS


app = Flask(__name__)
app.config.from_object(__name__)
# app.config.update(SESSION_COOKIE_SAMESITE=SESSION_COOKIE_SAMESITE, SESSION_COOKIE_SECURE=SESSION_COOKIE_SECURE)
# Session(app)
login_manager = LoginManager(app)
CORS(app, supports_credentials=SUPPORTS_CREDENTIALS)

from server import routes