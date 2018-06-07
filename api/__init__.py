import os, binascii
from flask import Flask
from flask_basicauth import BasicAuth
from .classes.passwordhelper import PasswordHelper

app = Flask(__name__)
app.secret_key = binascii.hexlify(os.urandom(24))

app.config['BASIC_AUTH_USERNAME'] = 'Ronald'
app.config['BASIC_AUTH_PASSWORD'] = 'Mutebi'

basic_auth = BasicAuth(app)
PH = PasswordHelper()

from . import controller