import re
from flask import jsonify, request
from passlib.hash import pbkdf2_sha256 as sha256
from app import app
from app.models.users_model import User
from app.controllers.db import DatabaseConnection
from app.validator import Validator
from flask_jwt_extended import (create_access_token, get_jwt_identity)
import datetime

db = DatabaseConnection()

class User_Controller:
    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    @staticmethod
    def login():
        db = DatabaseConnection()
        user_input = request.get_json(force=True)        
        username = user_input.get("user_name")
        password = user_input.get("user_password")
        validate = Validator.validate_user_login_credentials(username, password)
        if validate:
            return validate
        user = db.get_user(username)
        if user:
            verify_password = User_Controller.verify_hash(password, user[4])
            if verify_password:
                select = db.login_user(username, verify_password)
                if select:
                    expiry = datetime.timedelta(days=1)
                    user_data ={"username":username, "id":user[0], "role":user[5]}
                    access_token = create_access_token(identity = user_data, expires_delta=expiry)
                    return jsonify({
                        'success': f"You have successfully been logged in as {username}",
                        'access_token': access_token
                        }), 200
            return jsonify({'message':'Incorrect user name or password'}), 400
        return jsonify({'message':f"{username} does not exist"}), 400

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    def sign_up():
        """Register a user"""
        # db = DatabaseConnection()
        user_input = request.get_json(force=True) 
        user_name = user_input.get("user_name")          
        user_email = user_input.get("user_email")   
        user_mobile = user_input.get("user_mobile")
        user_password = user_input.get("user_password")  
        users = db.get_users()
        for user in users:
            if user_name == user[1]:
                return jsonify({'message':f"User {user_name} already exists"}), 400
            if user_email == user[2]:
                return jsonify({'message':"Email belongs to another account"}), 400

        validate_credentials = Validator.validate_user_credentials(user_name, user_email, user_password, user_mobile)
        if validate_credentials is not None:
            return validate_credentials
        if len(str(user_password)) < 9:
            return jsonify({'message':'Password must be more than 8 characters long'}), 400        
        mail = ['@', '.com']   
        for m in mail:               
            if not m in user_email:
                return jsonify({'message':'Please enter a valid email'}), 400

        user_password = User_Controller.generate_hash(user_password)
        new_user = User(user_name, user_email, user_mobile, user_password)
        db.insert_user(new_user.user_name, new_user.user_email, new_user.user_mobile, new_user.user_password)
        return jsonify({"message":f"User {user_name} successfully created"}), 201
    
    @staticmethod
    def get_registered_users():
        users_list = []
        current_user = get_jwt_identity()
        if current_user.get('role') == True:
            users = db.get_users()
            for user in users:
                user_dict = {
                    "user_id" : user[0],
                    "user_name": user[1],
                    "user_email": user[2],
                    "user_mobile": user[3],
                    "admin_status": user[5]
                }
                users_list.append(user_dict)
            return jsonify({'users':users_list}), 200
        return jsonify({'message':'You do not have access to this'}), 401

    @staticmethod
    def get_user(user_name):
        """Retrieve a particular user"""
        current_user = get_jwt_identity()
        user = db.get_user(user_name)
        if user:
            if current_user.get('username') == user_name:
                user_dict = {
                        "user_id" : user[0],
                        "user_name": user[1],
                        "user_email": user[2],
                        "user_mobile": user[3],
                        "admin_status": user[5],
                        "default_pickup_loc": user[6]
                        # "img":  standard_b64decode(user[7])
                    }
                return jsonify({"user":user_dict}), 200
            return jsonify({'message':'You do not have access to this'}), 401
        return jsonify({'message': f"{user_name} does not exist"}), 404

    @staticmethod
    def edit_user(user_name):
        """Modify a particular users details"""
        current_user = get_jwt_identity()
        user_input = request.get_json(force=True)        
        usermail = user_input.get("user_email")
        usermobile = user_input.get("user_mobile")
        defaultpickup = str(user_input.get("default_pickup_location"))

        user = db.get_user(user_name)
        if user:
            if current_user.get('username') == user_name:
                print(user_name, usermail, usermobile, defaultpickup)
                if not usermail or not usermobile:
                    return jsonify({'message':"Please fill in all fields"}), 400
                charset = re.compile('[A-Za-z]')
                if defaultpickup:
                    checkmatch = charset.match(defaultpickup)
                    if not checkmatch:
                        return jsonify({'message':"Default pickup location must be letters"}), 400
                if len(str(usermobile)) != 10:
                    return jsonify({'message':"Please enter a valid mobile contact"}), 400
                delete_mail = db.clear_data(user_name)
                if delete_mail:
                    users = db.get_users()
                    for a_user in users:
                        if usermail == a_user[2]:
                            return jsonify({'message':"Email belongs to another account"}), 400
                        db.edit_user(usermail, usermobile, defaultpickup, user_name)
                        return jsonify({"message":"Your details have successfully been updated"}), 200
                return jsonify({'message':"Something went wrong"}), 400
            return jsonify({'message':'You do not have access to this'}), 401
        return jsonify({'message': f"{user_name} does not exist"}), 404


    @staticmethod
    def no_user_parcels(user_name):
        current_user = get_jwt_identity()
        if current_user.get('username') == user_name:
            no = db.select_no_of_user_parcels(user_name)
            return jsonify({"number":no}), 200
        return jsonify({'message':'You do not have access to this'}), 401
    
    @staticmethod
    def no_delivered_user_parcels(user_name):
        current_user = get_jwt_identity()
        if current_user.get('username') == user_name:
            num = db.select_no_of_user_parcels_delivered(user_name)
            return jsonify({"number":num}), 200
        return jsonify({'message':'You do not have access to this'}), 401

    @staticmethod
    def no_pending_user_parcels(user_name):
        current_user = get_jwt_identity()
        if current_user.get('username') == user_name:
            num = db.select_no_of_user_parcels_pending(user_name)
            return jsonify({"number":num}), 200
        return jsonify({'message':'You do not have access to this'}), 401

    @staticmethod
    def no_intransit_user_parcels(user_name):
        current_user = get_jwt_identity()
        if current_user.get('username') == user_name:
            num = db.select_no_of_user_parcels_intransit(user_name)
            return jsonify({"number":num}), 200
        return jsonify({'message':'You do not have access to this'}), 401

    @staticmethod
    def no_cancelled_user_parcels(user_name):
        current_user = get_jwt_identity()
        if current_user.get('username') == user_name:
            num = db.select_no_of_user_parcels_cancelled(user_name)
            return jsonify({"number":num}), 200
        return jsonify({'message':'You do not have access to this'}), 401

    @staticmethod
    def switch_user_role(user_id):
        current_user = get_jwt_identity()
        print(current_user)
        if current_user.get('username') == 'admin':
            user = db.get_user_by_id(user_id)
            if user:
                if user[5] == True:
                    db.change_user_role_to_user(user_id)
                else:
                    db.change_user_role_to_admin(user_id)
                return jsonify({'message':'User role successfully changed'})
            return jsonify({'message':f"There is no user with ID {user_id}"})
        return jsonify({'message':'You do not have access to this'}), 401