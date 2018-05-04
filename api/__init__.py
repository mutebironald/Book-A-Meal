import os, binascii
from flask import Flask
from flask_basicauth import BasicAuth
from .classes.passwordhelper import PasswordHelper
from .classes.mockdbhelper import MockDBHelper as DBHelper
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = binascii.hexlify(os.urandom(24))

app.config['BASIC_AUTH_USERNAME'] = 'Ronald'
app.config['BASIC_AUTH_PASSWORD'] = 'Mutebi'

basic_auth = BasicAuth(app)
login_manager = LoginManager(app)

PH = PasswordHelper()
DB = DBHelper()

from . import bookameal