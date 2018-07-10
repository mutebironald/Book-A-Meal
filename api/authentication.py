import jwt
import datetime
from flask import request

from . import app


class Token:
    def generate_token(self, user_id):
        """Generates the access token"""
        try:
            payload = {"exp": datetime.datetime.utcnow(
            ) + datetime.timedelta(minutes=60), "sub": user_id}

            jwt_string = jwt.encode(
                payload,
                app.config["SECRET_KEY"],
                algorithm="HS256"
            )
            return (jwt_string).decode("utf-8")

        except Exception as e:
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            payload = jwt.decode(token, app.config["SECRET_KEY"])
            # return payload["sub"]
            return True

        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return False
