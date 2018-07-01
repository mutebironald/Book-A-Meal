from . import auth_blueprint

from flask.views import MethodView
from flask import make_response, request, jsonify
from app.models import User
import re

class RegistrationView(MethodView):
    """This class registers a new user."""

    def post(self):
        """Handle a POST request for this view. Url ---> /auth/register"""
        user = User.query.filter_by(email=request.data['email']).first()

        if not user:
            try:
                message = "Wrong email or password"
                status_code = 400
                post_data = request.data
                email = post_data['email']
                password = post_data['password']
                if email and password:
                    if not re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", email):
                        return message, status_code
                    if password.strip() == "":
                        return message, status_code
                    if len(password) < 5:
                        return "Password should be more than 5 characters"
                    user = User(email=email, password=password)
                    user.save()
                    response = {
                        'message': 'You registered successfully.'
                    }
                    return make_response(jsonify(response)), 201
            
            except Exception as e:
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 401

        else:
            response = {
                'message': 'User already exists. Please login.'
            }

            return make_response(jsonify(response)), 202

registration_view = RegistrationView.as_view('register_view')

class LoginView(MethodView):
    """This class-based view handles user login and access token generation."""

    def post(self):
        """Handle POST request for this view. Url --> /auth/login"""
        try:
            user = User.query.filter_by(email=request.data['email']).first()

            if user and user.password_is_valid(request.data['password']):
                access_token = user.generate_token(user.id)
                if access_token:
                    response = {
                        'message': 'You logged in successfully.',
                        'access_token': access_token.decode()
                    }
                    return make_response(jsonify(response)), 200
            else:
                response ={
                    'message': 'Invalid email or password, Please try again'
                }
                return make_response(jsonify(response)), 401
        
        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500

registration_view = RegistrationView.as_view('registration_view')
login_view = LoginView.as_view('login_view')


auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST']
    )

auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)
