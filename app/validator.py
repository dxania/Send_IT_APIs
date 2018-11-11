import re
from flask import jsonify
from app import app
from app.models.users_model import users, User


class Validate:
    @staticmethod
    def validate_user(user_name):
        if not user_name or user_name.isspace():
            return jsonify({'message': "User name is required"}), 200

        charset = re.compile('[A-Za-z]')
        checkmatch = charset.match(user_name)
        if not checkmatch:
            return jsonify({'message':'User name must be letters'}), 200
       
        for user in users:
            user_dict = user.to_dict()
            if user_dict['user_name'] == user_name:
                return jsonify({'message':f"User {user_name} already exists"}), 200
     

    # @staticmethod
    def validate_password(password):
        if not password or password.isspace():
            return jsonify({'message':'Password is required'}), 200
        
        charset2 = re.compile('[A-Za-z0-9]')
        checkmatch = charset2.match(password)
        if not checkmatch:
            return jsonify({'message':'Password should be letters and/or numbers'}), 200

       