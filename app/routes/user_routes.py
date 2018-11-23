from app import app
from flask import jsonify
from app.controllers.user_controller import User_Controller
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)


@app.route('/api/v1/auth/login', methods = ['POST'])
def login():
    return User_Controller.login()


@app.route('/api/v1/auth/signup', methods =['POST'])
def user_signup():
    return User_Controller.sign_up()

@app.route('/api/v1/users', methods = ['GET'])
@jwt_required
def get_registered_users():
    return User_Controller.get_registered_users()

@app.route('/api/v1/users/<int:user_id>/role', methods = ['PUT'])
@jwt_required
def change_user_role(user_id):
    return User_Controller.switch_user_role(user_id)