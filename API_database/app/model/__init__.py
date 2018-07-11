from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta
from flask import jsonify, make_response

from app.__init__ import db, secret
import datetime

from app import db