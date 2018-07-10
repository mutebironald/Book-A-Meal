from functools import wraps
from flask import request,jsonify

from . import authentication

auth = authentication.Token()

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        access_token = request.headers.get("Authorization")
        if access_token:
            try:
                user_id = auth.decode_token(access_token)

            except Exception as e:
                return str(e)

            else:
                if user_id and isinstance(user_id, int):
                    return f(*args, **kwargs)
                else:
                    return jsonify({"message": "Invalid token"}), 401
        return jsonify({"message": "Token is missing"}), 400
    return wrap
