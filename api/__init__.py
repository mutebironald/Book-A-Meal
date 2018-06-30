import os, binascii
from flask import Flask
from .classes.passwordhelper import PasswordHelper

app = Flask(__name__)
app.secret_key = binascii.hexlify(os.urandom(24))
PH = PasswordHelper()

from . import controller