from flask_api import FlaskAPI

from flask import request, jsonify, abort



def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object("config")
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    return app

