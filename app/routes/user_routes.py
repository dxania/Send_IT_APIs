from app import app
from flask import jsonify
from app.controllers.user_controller import User_Controller
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)


@app.route('/api/v1/auth/login', methods = ['POST'])
def login():
    return User_Controller.login()


@app.route('/api/v1/users/logged', methods = ['GET'])
@jwt_required
def get_logged_in_users():
    current_user = get_jwt_identity()
    if current_user == 'admin':
        return User_Controller.get_logged_in_users()
    return jsonify({'message':'Invalid request! login or use the right access token'})


@app.route('/api/v1/auth/signup', methods =['POST'])
def user_signup():
    return User_Controller.sign_up()

@app.route('/api/v1/users', methods = ['GET'])
def get_registered_users():
    current_user = get_jwt_identity()
    if current_user == 'admin':
        return User_Controller.get_registered_users()
    return jsonify({'message':'Invalid request! login or use the right access token'})