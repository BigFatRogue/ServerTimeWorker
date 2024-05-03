import os

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE = os.path.join(PROJECT_ROOT, 'db.db')
SECRET_KEY = '01a439747c9da4e08bc0da93174d764c3d5eed5d'
SESSION_TYPE = 'filesystem'
DEBUG = False
THREADED = True
SESSION_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SECURE = True
SUPPORTS_CREDENTIALS = True
HOST = '0.0.0.0'
PORT = 5000