
from flask import Flask, request, jsonify,abort

app = Flask(__name__)


menu = [{"id": 1, "name": "Mushroom Soup","description": "Tasty and yammy.", "price": "UGX 12,000"},{"id": 2,"name": "Fufu","description": "Tasty and yammy.","price": "UGX 18,000"}]

MEALS =[{'meal_name':'Kikomando', 'price':1700, 'user_id':'id'},
        {'meal_name':'Posho and chicken', 'price':3400, 'user_id':'id'}]


@app.route('/api/v1/meals', methods=['GET'])
def get_all_meals():
	return jsonify({'meals': MEALS})

@app.route('/api/v1/meals/<int:meal_id>', methods=['GET'])
def get_particular_meal(meal_id):
	meal = []
	for meal in MEALS: 
		if meal['id'] == meal_id:
			return jsonify({'meal': meal})
	return jsonify({'message': 'Meal not found'})
	
@app.route('/api/v1/meals', methods=['POST'])
def meal_creation():
	if not request.json or not 'name' in request.json:
		abort(404)
	meal = {
		'id': MEALS[-1]['id'] + 1 ,
		'name': request.json['name'],
		'description': request.json['description'],
		'price': request.json['price']
	}
	MEALS.append(meal)
	return jsonify({'meal': meal}), 201

@app.route('/api/v1/meals/<int:meal_id>', methods=['PUT'])
def updating_specific_meal(meal_id):
	meal = [meal for meal in MEALS if meal['id'] == meal_id]
	if len(meal) == 0:
		abort(404)
	if not request.json:
		abort(404)
	if 'name' in request.json and type(request.json['name']) != unicode:
		abort(400)
	if 'description' in request.json and type(request.json['description']) is not unicode:
		abort(400)
	if 'admin' in request.json and type(request.json['admin']) is not bool:
		abort(400)
	meal[0]['name'] = request.json.get('name', meal[0]['name'])
	meal[0]['description'] = request.json.get('description', meal[0]['description'])
	meal[0]['admin'] = request.json.get('admin', meal[0]['admin'])
	return jsonify({'meal': meal[0]})
	
@app.route('/api/v1/meals/<int:meal_id>', methods=['DELETE'])
def remove_meal(meal_id):
	for meal in MEALS: 
		if meal['id'] == meal_id:
			meal.remove(meal[0])
			return jsonify({'meals': MEALS})
	return jsonify({'message': 'meal not found'})


