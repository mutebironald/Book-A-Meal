# class User(db.Model):
#     """Defines the 'User' model mapped to database table 'user'."""
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(145), nullable=False, unique=True)
#     password = db.Column(db.String(100), nullable=False)
#     admin = db.Column(db.Boolean, default=False)
#     orders = db.relationship('Order', backref='user')

#     def __init__(self, email, password):
#         """Initialize the user with an email and a password."""
#         self.email = email
#         self.password = Bcrypt().generate_password_hash(password).decode('utf-8')

#     def password_is_valid(self, password):
#         """Checks the password against its hash to validate the user's password"""
#         return Bcrypt().check_password_hash(self.password, password)

#     def __repr__(self):
#         """Returns a User model representation"""
#         return "User (%d, %s, %s, %s)" % (
#             self.id, self.email, self.admin, self.orders)

#     def save(self):
#         """Save a user to the database."""
#         db.session.add(self)
#         db.session.commit()

#     def generate_token(self, user_id):
#         """Generates the access token"""
#         try:
#             payload = {
#                 'exp': datetime.datetime.utcnow() + timedelta(minutes=60),
#                 'sub': user_id
#             }

#             jwt_string = jwt.encode(
#                 payload,
#                 secret,
#                 algorithm='HS256'
#             )

#             return jwt_string

#         except Exception as e:
#             return str(e)

#     @staticmethod
#     def decode_token(token):
#         """Decodes the access token from the Authorization header."""
#         try:
#             payload = jwt.decode(token, secret)
#             return payload['sub']

#         except jwt.ExpiredSignatureError:
#             return "Expired token. Please login to get a new token."

#         except jwt.InvalidTokenError:
#             return "Invalid token. Please register or login."
