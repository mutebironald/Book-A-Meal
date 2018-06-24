import jwt
import datetime
from . import app

from functools import wraps
from flask import  request

class Token:
    def generate_token(self, user_id):
        """Generates the access token"""
        try:
            payload = {
                'exp':datetime.datetime.utcnow()  + datetime.timedelta(minutes=60),
                'sub': user_id
                }
            
            jwt_string = jwt.encode(
                payload,
                app.config['SECRET_KEY'],
                algorithm='HS256'
                )
            return (jwt_string).decode('utf-8')

        except Exception as e:
            return str(e)    

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'])
            return payload['sub']

        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return False

    @staticmethod
    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            access_token = request.headers.get("Authorization")
            if access_token:
                print(access_token)
                user_id = Token.decode_token(access_token)
            return f(*args, **kwargs)
        return decorated_function
            