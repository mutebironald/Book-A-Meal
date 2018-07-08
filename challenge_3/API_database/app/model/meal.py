# class Meal(db.Model):
#     """Defines the 'Meal' model mapped to database table 'meal'."""
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(46), nullable=False, unique=True)
#     price = db.Column(db.Integer, nullable=False)
#     menus = db.relationship('Menu', backref='meal')

#     def __init__(self, name, price):
#         """Initialises the meal model"""
#         self.name = name
#         self.price = price
 
#     def save(self):
#         """Saves item to the Meal table"""
#         db.session.add(self)
#         db.session.commit()

#     def delete(self):
#         """Removes item from meal table"""
#         db.session.delete(self)
#         db.session.commit()

#     @staticmethod
#     def get_meals():
#         """Retrieves all meals present in the meal table"""
#         results = []
#         meals = Meal.query.all()
#         if meals:
#             for meal in meals:
#                 obj = {
#                     "id": meal.id,
#                     "name": meal.name,
#                     "price": meal.price,
#                 }
#                 results.append(obj)
#             response = jsonify(results)
#             response.status_code = 200
#             return response
#         else:
#             return "No meals present", 400

#     @staticmethod
#     def get_meal(id):
#         meal = Meal.query.filter_by(id=id).first()
#         if not meal:
#             return make_response("That meal is not present", 400)
#         results = []
#         obj = {
#             'id': meal.id,
#             'name': meal.name,
#             'price': meal.price
#         }
#         results.append(obj)
#         return make_response(jsonify(results), 200)

#     @staticmethod
#     def create_meal(name, price):
#         meal = Meal(name, price)
#         meal.save()
#         response = jsonify({
#             'id': meal.id,
#             'name': meal.name,
#             'price': meal.price,
#         })
#         response.status_code = 201
#         return response

#     @staticmethod
#     def update_meal(id, name, price):
#         meal = Meal.query.filter_by(id=id).first()
#         if not meal:
#             abort(404)

#         meal.name = name
#         meal.price = price
#         meal.save()
#         response = jsonify({
#             'id': meal.id,
#             'name': meal.name,
#             'price': meal.price
#         })

#         response.status_code = 200
#         return response

#     @staticmethod
#     def delete_meal(id):
#         meal = Meal.query.filter_by(id=id).first()
#         if meal:
#             Meal.delete(meal)
#             response = make_response(
#                 'The meal has been deleted', 200)
#             return response
#         return "The meal specified is not present", 400

#     def __repr__(self):
#         """Returns a representation of the meals"""
#         return "Meal (%d, %s, %s )" % (
#             self.id, self.name, self.price)
