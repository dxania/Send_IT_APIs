import json
import unittest
from app import app
from app.routes.user_routes import *
from app.controllers.db import DatabaseConnection
from tests.test_create import Base


class Endpoints(Base):
    """
    Tests all aspects of endpoints
    Tests include: registering a user, logging in a user, logging in an admin.  
    """

    def test_sign_up(self):
        self.sign_up()
        
    def test_admin_login(self):
        self.admin_login()

    def test_user_login(self):
        self.user_login()

    def test_get_registered_users(self):
        self.admin_login()
        self.user_login()

        get_users = self.app_client.get('/api/v1/users', headers={'Authorization': f"Bearer {self.admin_access_token}"})
        self.assertEqual(get_users.status_code, 200)

    def test_no_registered_users(self):
        self.admin_login()
        get_users = self.app_client.get('/api/v1/users', headers={'Authorization': f"Bearer {self.admin_access_token}"})
        self.assertEqual(get_users.status_code, 200)
        get_response = json.loads(get_users.data.decode())
        self.assertEqual(get_response['message'], 'There are no registered users')

    def test_unauthorized_user_get_registered_users(self):
        self.user_login()

        get_users = self.app_client.get('/api/v1/users', headers={'Authorization': f"Bearer {self.user_access_token}"})
        self.assertEqual(get_users.status_code, 401)
        get_response = json.loads(get_users.data.decode())
        self.assertEqual(get_response['message'], 'You do not have access to this')

class Set(Base):
    """
    Tests all aspects of setting attributes
    Tests include: setting attributes of wrong type, 
    setting attributes outside their constraints, setting empty attributes.
    """
    def test_user_name_required(self):
        user ={
            "user_name" : "",
            "password": "winx"
        }
        post_request = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps(user))
        response = json.loads(post_request.data.decode())
        self.assertEqual("User name/password required", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_user_name_str(self):
        user ={
            "user_name" : 55,
            "password": "winx"
        }
        post_request = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps(user))
        response = json.loads(post_request.data.decode())
        self.assertEqual("User name/password must be strings", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_user_name_letters(self):
        user ={
            "user_name" : "55",
            "password": "winx"
        }
        post_request = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps(user))
        response = json.loads(post_request.data.decode())
        self.assertEqual("User name/password must be letters", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_user_name_exists(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', 
            data=json.dumps({"user_name":"daniella", "password":"danny"}))
        self.assertEqual(create_user.status_code, 201)
        user ={
            "user_name" : "daniella",
            "password": "danny"
        }
        post_request = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps(user))
        response = json.loads(post_request.data.decode())
        self.assertEqual("User daniella already exists", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_password_required(self):
        user ={
            "user_name" : "wake",
            "password": ""
        }
        post_request = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps(user))
        response = json.loads(post_request.data.decode())
        self.assertEqual("User name/password required", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_password_letters_or_numbers(self):
        user ={
            "user_name" : "dan",
            "password": "#123"
        }
        post_request = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps(user))
        response = json.loads(post_request.data.decode())
        self.assertEqual("User name/password must be letters", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_password_str(self):
        user ={
            "user_name" : "dan",
            "password": 123
        }
        post_request = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps(user))
        response = json.loads(post_request.data.decode())
        self.assertEqual("User name/password must be strings", response['message'])
        self.assertEqual(post_request.status_code, 400)    
  

if __name__ == ('__main__'):
    unittest.main()