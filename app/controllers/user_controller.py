import re
from flask import jsonify, request
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token)
from app import app
from app.models.users_model import users, User
from app.controllers.db import DatabaseConnection
from app.validator import Validator
from flask_jwt_extended import (create_access_token, get_jwt_identity)

db = DatabaseConnection()

class User_Controller:
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    def login():
        db = DatabaseConnection()
        user_input = request.get_json(force=True)        
        username = user_input.get("user_name")
        validate = Validator.validate_username(username)
        if validate is not None:
            return validate
        password = user_input.get("password")
        validate = Validator.validate_password(password)
        if validate is not None:
            return validate

        user = db.get_user(username)
        if user is not None:
            verify_password = User_Controller.verify_hash(user_input.get("password"), user[2])
            select = db.login_user(username, verify_password)
            if select is not None:
                access_token = create_access_token(identity = username)
                return jsonify({
                    'message': f"You have successfully been logged in as {username}",
                    'access_token': access_token
                    }), 200
            return jsonify({'message':'Incorrect user name or password'}), 400
        return jsonify({'message':f"{username} does not exist"}), 400

    def generate_hash(password):
        return sha256.hash(password)

    def sign_up():
        """Register a user"""
        db = DatabaseConnection()
        
        user_input = request.get_json(force=True) 
        user_name = user_input.get("user_name")
        validate = Validator.validate_username(user_name)
        if validate is not None:
            return validate
        
        users = db.get_users()
        for user in users:
            if user_name == user[1]:
                return jsonify({'message':f"User {user_name} already exists"}), 200
       
        password = user_input.get("password")
        validate = Validator.validate_password(password)
        if validate is not None:
            return validate
        
        password = User_Controller.generate_hash(password)
        new_user = User(user_name,password)
        db.insert_user(new_user.user_name, new_user.password)
        return jsonify({"user_successfully_created":new_user.to_dict()}), 201
    
    def get_registered_users():
        current_user = get_jwt_identity()
        if current_user == 'admin':
            users = db.get_users()
            if users is not None:
                return jsonify(users)
            return jsonify({'message':'There are no registered users'})
        return jsonify({'message':'You do not have access to this'})
