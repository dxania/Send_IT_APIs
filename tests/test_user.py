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

    # def test_no_registered_users(self):
    #     self.admin_login()
    #     get_users = self.app_client.get('/api/v1/users', headers={'Authorization': f"Bearer {self.admin_access_token}"})
    #     get_response = json.loads(get_users.data)
    #     self.assertEqual(get_users.status_code, 404)
    #     self.assertEqual(get_response['message'], 'There are no registered users')

    def test_unauthorized_user_get_registered_users(self):
        self.user_login()
        get_users = self.app_client.get('/api/v1/users', headers={'Authorization': f"Bearer {self.user_access_token}"})
        self.assertEqual(get_users.status_code, 401)
        get_response = json.loads(get_users.data)
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
            "user_email":"kxania@gmail.com",
            "user_mobile" : "0777777777",
            "user_password": "thepasswords"
        }
        post_request = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps(user))
        response = json.loads(post_request.data.decode())
        self.assertEqual("User name required", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_user_name_letters(self):
        user ={
            "user_name" : "55",
            "user_email":"kxania@gmail.com",
            "user_mobile" : "0777777777",
            "user_password": "thepasswords"
        }
        post_request = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps(user))
        response = json.loads(post_request.data.decode())
        self.assertEqual("User name must be letters", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_user_name_exists(self):
        self.sign_up()
        user ={
            "user_name" : "eve",
            "user_email":"kxania@gmail.com",
            "user_mobile" : "0777777777",
            "user_password": "danniellas"
        }
        post_request = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps(user))
        response = json.loads(post_request.data.decode())
        self.assertEqual("User eve already exists", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_password_required(self):
        user ={
            "user_name" : "wake",
            "user_email":"kxania@gmail.com",
            "user_mobile" : "0777777777",
            "user_password": ""
        }
        post_request = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps(user))
        response = json.loads(post_request.data.decode())
        self.assertEqual("Password required", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_password_length(self):
        user ={
            "user_name" : "wake",
            "user_email":"kxania@gmail.com",
            "user_mobile" : "0777777777",
            "user_password": "123"
        }
        post_request = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps(user))
        response = json.loads(post_request.data.decode())
        self.assertEqual("Password must be more than 8 characters long", response['message'])
        self.assertEqual(post_request.status_code, 400)  

    def test_email_required(self):
        user ={
            "user_name" : "wake",
            "user_email":"",
            "user_mobile" : "0777777777",
            "user_password": "qqqqqqqqqqqq"
        }
        post_request = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps(user))
        response = json.loads(post_request.data.decode())
        self.assertEqual("Email required", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_email_valid(self):
        user ={
            "user_name" : "wake",
            "user_email":"cakes",
            "user_mobile" : "0777777777",
            "user_password": "8characters"
        }
        post_request = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps(user))
        response = json.loads(post_request.data.decode())
        self.assertEqual("Please enter a valid email", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_mobile_required(self):
        user ={
            "user_name" : "wake",
            "user_email":"kxania@gmail.com",
            "user_password": "qqqqqqqqqqqq"
        }
        post_request = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps(user))
        response = json.loads(post_request.data.decode())
        self.assertEqual("Mobile Contact required", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_mobile_valid(self):
        user ={
            "user_name" : "wake",
            "user_email":"cakes",
            "user_mobile" : "07777",
            "user_password": "8characters"
        }
        post_request = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps(user))
        response = json.loads(post_request.data.decode())
        self.assertEqual("Please enter a valid mobile contact", response['message'])
        self.assertEqual(post_request.status_code, 400)
  

if __name__ == ('__main__'):
    unittest.main()