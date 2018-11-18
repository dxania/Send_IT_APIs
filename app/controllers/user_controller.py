import re
from flask import jsonify, request
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token)
from app import app
from app.models.users_model import users, User

logged_in_users = []
   
class User_Controller:
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    def login():
        admin_name = "admin"
        admin_password = "root"
        user_input = request.get_json(force=True)
        if user_input.get("user_name") == admin_name and user_input.get("password") == admin_password:
            access_token = create_access_token(identity = admin_name)
            return jsonify({
                'message': 'You have been logged in as admin',
                'access_token': access_token
                }), 200
        else:
            for user in users:
                user_dict = user.to_dict()
                if user_dict['user_name'] == user_input.get("user_name") and User_Controller.verify_hash(user_input.get("password"), user_dict['password']):
                    logged_in_users.append(user)
                    user_access_token = create_access_token(identity = user_input.get("user_name"))
                    return jsonify({
                        'message': f"You have successfully been logged in as {user_input.get('user_name')}",
                        'access_token': user_access_token
                        }), 200
        return jsonify({'message':'Incorrect user name or password'}), 400


    def generate_hash(password):
        return sha256.hash(password)

    def sign_up():
        """Register a user"""
        user_id = len(users) + 1
        user_input = request.get_json(force=True) 
        user_name = user_input.get("user_name")
        charset = re.compile('[A-Za-z]')
        checkmatch = charset.match(user_name)

        if not user_name:
            return jsonify({'message':'Please enter a user name'}), 400
        else:
            if not isinstance(user_name, str):
                return jsonify({'message':'User name must be a string'}), 400
            else:
                if not checkmatch:
                    return jsonify({'message':'User name must be letters'}), 400
                else:
                    for user in users:
                        user_dict = user.to_dict()
                        if user_dict['user_name'] == user_name:
                            return jsonify({'message':f"User {user_name} already exists"}), 400
       
        password = user_input.get("password")
        charset2 = re.compile('[A-Za-z0-9]')
        checkmatch = charset2.match(password)
        if not password:
            return jsonify({'message':'Password is required'}), 400
        else:
            if not isinstance(password, str):
                return jsonify({'message':'Password must be a string'})
            elif not checkmatch:
                return jsonify({'message':'Password should be letters and/or numbers'}), 400
            
        hashed_password = User_Controller.generate_hash(password)
        user = User(user_id, user_name, hashed_password)
        users.append(user)
        return jsonify({"user_successfully_created":user.to_dict()}), 201
    

    def get_logged_in_users():
        logged = []
        for user in logged_in_users:
            logged.append(user.to_dict())
        if logged_in_users:
            return jsonify(logged)
        return jsonify({'message':'There are no logged in users'})

    def get_registered_users():
        users_list = []
        for user in users:
            users_list.append(user.to_dict())
        if users_list:
            return jsonify(users_list)
        return jsonify({'message':'There are no registered users'})
