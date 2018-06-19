import os, binascii
from flask import Flask
from .classes.passwordhelper import PasswordHelper
from .classes.mockdbhelper import MockDBHelper as DBHelper

app = Flask(__name__)
app.secret_key = binascii.hexlify(os.urandom(24))

PH = PasswordHelper()
DB = DBHelper()

from . import bookameal