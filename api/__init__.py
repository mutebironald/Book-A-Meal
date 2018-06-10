import os, binascii
from flask import Flask
from .classes.passwordhelper import PasswordHelper

app = Flask(__name__)
app.secret_key = binascii.hexlify(os.urandom(24))
#app.secret_key = 'hahaha_not_hackable'

PH = PasswordHelper()

from . import controller