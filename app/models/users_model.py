import json
from flask import jsonify

users = [
    {
        "user_id" : 1,
        "user_name" : "ney",
        "password": "pro"
    },
    {
        "user_id" : 2,
        "user_name" : "dee",
        "password": "io"
    }
]

class Users():
    """Users class defining 
    the parcel models
    """
    def __init__(self, user_id, user_name, password):
        self.user_id = len(parcels) + 1
        self.user_name = user_name
        self.password = password

        
    def create_a_user(self):
 
        user = {
            "user_id" : self.user_id,
            "user_name" : self.user_name,
            "password": self.password
        }

        users.append(user)
        return jsonify({"user successfully created":user})


   
