# import json
# from flask import jsonify

class User():
    """Users class defining the user model"""
    def __init__(self, user_name, user_email, user_mobile, user_password):
        self.user_name = user_name
        self.user_email = user_email
        self.user_mobile = user_mobile
        self.user_password = user_password
        self.admin_status = False

        
    def to_dict(self):
        """Convert the user object to a dictionary"""
        user = {
            "user_name" : self.user_name,
            # "user_password": self.user_password,
            "admin_status": self.admin_status
        }
        return user


   
