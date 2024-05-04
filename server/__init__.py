from server.my_sitting import *
from flask import Flask
from flask_login import LoginManager, logout_user, login_user
from flask_cors import CORS


app = Flask(__name__)
app.config.from_object(__name__)
login_manager = LoginManager(app)

CORS(app, supports_credentials=SUPPORTS_CREDENTIALS)

from server import routes, routes_admin