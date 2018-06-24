import hashlib
import os
import base64


class PasswordHelper:
    """A class to deal with passwords"""

    def get_hash(self, plain):
        """"Method to generate password hash"""
        return hashlib.sha512(plain.encode('utf-8')).hexdigest()

    def get_salt(self):
        """This method generates a random salt"""
        return base64.b64encode(os.urandom(20))

    def validate_password(self, plain, salt, expected):
        """Check is password entered is equal to that stored"""
        return self.get_hash(plain + str(salt)) == expected
