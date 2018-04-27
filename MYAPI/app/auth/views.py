from flask import render_template, jsonify, request, make_response

from . import auth

import re

from app.models import User, USERS

@auth.route('/')
@auth.route('/api/v1/auth/')
def welcome():
    return jsonify({'msg': "Welcome to Book-A-Meal"})

@auth.route('/api/v1/auth/login', methods=['POST'])
def loginpage():
    """
    Render the login template on the /login
    """
       
    email = request.json_get['email']
    password = request.json_get['password']
    password2 = request.json_get['password2']
    if not re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", email):
        error = {"message": "Invalid Email"}
        return jsonify(error)
    if len(password) < 9:
        error = {"message": "Make your password a bit longer"}
        return jsonify(error)
    if password == password2:
        error = {"message":"Invalid Password"}
        return jsonify(error)
    sign_in = User(email, password)


    if sign_in:
        response = {'message': 'You have successfully signed up'}
        return make_response(response), 201
    else:
        response = {'message': 'You are not registered'}
        return make_response(response), 200
    


@auth.route('/api/v1/auth/register', methods=['POST'])
def register():
    """
    Render the registration template on the /register route
    """
    email = request.json_get['email']
    password = request.json_get['password']
    new_user = User(email, password) 
    new_user.register_user(new_user)  

    

    