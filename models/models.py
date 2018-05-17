from sqlalchemy import SQLAlchemy
import datetime

# initialize SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    """Defines a user model mapped to a database table 'user'"""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(145), unique=True)
    password = db.Column(db.String(170))
    admin = db.Column(db.Boolean, default=False)
    orders = db.relationship('Order', ackref='user', lazy='dynamic')

    def __repr__(self):
        return "User(%d, %s, %s, %s, %s)" %(self.id, self.email, self.password, self.admin, self.orders)
        
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(145), unique=True)
    user_id = db.Column(db.Integer)
    admin = db.Column(db.Boolean, default=True)
    meals = db.relationship('Meal', backref='Admin')
    menu = db.relationship('Menu', backref='Admin')

    def __repr__(self):
        return "Admin (%d, %s, %s, %s, %s, %s)" %(self.id, self.email, self.user_id, self.admin, self.meals, self.menu) 

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    menu = db.relationship('menu', backref='meal')

    def __repr__(self):
        return "Meal (%d, %s, %s, %s)" %(self.id, self.name, self.price, self.admin_id) 

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(60), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'))
    day = db.Column(db.String(50), default=datetime.datetime.today())
    orders = db.relationship('order', backref='menu')

    def __repr__(self):
        "Menu (%d, %s, %s, %s, %s)" %(self.id, self.name, self.owner_id, self.meal_id, self.day)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    menu_name = db.Column(db.Integer, db.ForeignKey('menu.name'))
    meal_id = db.Column(db.Integer)
    admin_id = db.Column(db.Integer)
    time_created = db.Column(db.String)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return "Order (%d, %s, %s, %s, %s)" %(self.id, self.menu_name, self.meal_id, self.time_created, self.customer_id)


def load_db(db):
    """create database tables and insert records"""
    db.drop_all()
    db.create_all()

    db.session.commit 