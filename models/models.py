from sqlalchemy import SQLAlchemy

# initialize SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    """Defines a user model mapped to a database table 'user'"""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(45), unique=True)
    password = db.Column(db.String(170))
    admin = db.Column(db.Boolean, default=False)
    orders = db.relationship('Order', ackref='user', lazy='dynamic')

    def __repr__(self):
        return "User(%d, %s, %s, %s, %s)" %(self.id, self.email, self.password, self.admin, self.orders)
        