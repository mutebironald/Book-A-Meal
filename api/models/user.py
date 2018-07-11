import datetime
import re
from flask import make_response, jsonify

from api import PH
from ..authentication import Token


class User:
    """A class for all users"""

    def __init__(self):
        """Initialises the user class"""
        self.users = []
        self.id = 1

    def get_user(self, email):
        """Retrieves a user from a list of users"""
        available_user = [
            user for user in self.users if user["email"] == email]
        if available_user:
            return available_user[0]
        return False

    def verify_login(self, email, password):
        """validates login details"""
        response_message = "You are now logged in"
        response_code = 200
        absent_code = 401
        stored_user = self.get_user(email)
        if stored_user and PH.validate_password(
                password, stored_user["salt"], stored_user["hashed"]):
            access_token = Token().generate_token(stored_user["id"])
            return make_response(
                jsonify({"token": access_token, "message": response_message}), response_code)
        return make_response("Please register then login", absent_code)

    @staticmethod
    def validate_email_and_password(email, password):
        """Ensures signup with correct credentials"""
        if not re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", email):
            return False
        if password.strip() == "":
            return False
        if len(password) < 5:
            return False
        return True

    def add_user(self, email, salt, hashed):
        """Helps add a user to the list of users"""
        if self.get_user(email):
            return False
        new_user = {
            "id": self.id,
            "email": email,
            "salt": salt,
            "hashed": hashed}
        self.users.append(new_user)
        self.id += 1
        return new_user
