import json
from flask import jsonify

users = []

class User():
    """Users class defining the user model"""
    def __init__(self, user_name, email, password):
        self.user_name = user_name
        self.email = email
        self.password = password
        self.admin = False

        
    def to_dict(self):
        user = {
            "user_name" : self.user_name,
            "password": self.password,
            "admin": self.admin
        }
        return user


   
