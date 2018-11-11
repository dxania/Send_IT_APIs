import re
from flask import jsonify, request
from app import app
from app.models.users_model import users, User

   
class User_Controller:
     
    def create_user():
        """Create a user function"""
        user_id = len(users) + 1
        user_input = request.get_json(force=True)       
        user_name = user_input.get("user_name")
        if not user_name or user_name.isspace():
            return jsonify({'message': "User name is required"}), 400

        charset = re.compile('[A-Za-z]')
        checkmatch = charset.match(user_name)
        if not checkmatch:
            return jsonify({'message':'User name must be letters'}), 400
       
        for user in users:
            user_dict = user.to_dict()
            if user_dict['user_name'] == user_name:
                return jsonify({'message':f"User {user_name} already exists"}), 400
        
        password = user_input.get("password")
        if not password or password.isspace():
            return jsonify({'message':'Password is required'}), 400
        
        charset2 = re.compile('[A-Za-z0-9]')
        checkmatch = charset2.match(password)
        if not checkmatch:
            return jsonify({'message':'Password should be letters and/or numbers'}), 400
            
        user = User(user_id, user_name, password)
        users.append(user)
        return jsonify({"user_successfully_created":user.to_dict()}), 201
    
