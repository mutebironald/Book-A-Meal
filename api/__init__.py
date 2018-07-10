import os
import binascii
from flask import Flask
from .models.passwordhelper import PasswordHelper

app = Flask(__name__)
app.secret_key = binascii.hexlify(os.urandom(24))
PH = PasswordHelper()

from . import views