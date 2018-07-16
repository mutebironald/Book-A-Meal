import jwt
from datetime import datetime, timedelta
import os, binascii

secret = binascii.hexlify(os.urandom(24))
class Token:
    def generate_token(self, user_id):
            """Generates the access token"""
            try:
                payload = {
                    "exp": datetime.utcnow() + timedelta(minutes=60),
                    "sub": user_id
                }

                jwt_string = jwt.encode(
                    payload,
                    secret,
                    algorithm="HS256"
                )

                return jwt_string

            except Exception as e:
                return str(e)
      
    def decode_token(self, token):
        """Decodes the access token from the Authorization header."""
        try:
            payload = jwt.decode(token, secret)
            return payload["sub"]

        except jwt.ExpiredSignatureError:
            return "Expired token. Please login to get a new token."

        except jwt.InvalidTokenError:
            return "Invalid token. Please register or login."
