import json
import unittest
from app import app
from app.routes.user_routes import *

test_user ={
    "user_name" : "dee",
	"password": "winx"
}

class Base(unittest.TestCase):
    """Base class for tests. 
    This class defines a common `setUp` method that defines attributes which are used in the various tests.
    """

    def setUp(self):
        self.app_client = app.test_client()


class Endpoints(Base):
    """
    Tests all aspects of endpoints
    Tests include: creating a parcel delivery order, getting all parcel delivery orders,getting a particular 
    parcel delivery order, canceling a parcel delivery order, getting all parcel delivery orders by a specific user.  
    """

    def test_create_user(self):
        create_user = self.app_client.post("/api/v1/users", content_type='application/json', data=json.dumps(test_user))
        self.assertEqual(create_user.status_code, 201)


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
        post_request = self.app_client.post("/api/v1/users", content_type='application/json', data=json.dumps(user))
        response = json.loads(post_request.data.decode())
        self.assertEqual("User name is required", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_user_name_letter(self):
        user ={
            "user_name" : "55",
            "password": "winx"
        }
        post_request = self.app_client.post("/api/v1/users", content_type='application/json', data=json.dumps(user))
        response = json.loads(post_request.data.decode())
        self.assertEqual("User name must be letters", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_user_name_letter(self):
        user ={
            "user_name" : "dee",
            "password": "winx"
        }
        post_request = self.app_client.post("/api/v1/users", content_type='application/json', data=json.dumps(user))
        response = json.loads(post_request.data.decode())
        self.assertEqual("User dee already exists", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_password_required(self):
        user ={
            "user_name" : "wake",
            "password": ""
        }
        post_request = self.app_client.post("/api/v1/users", content_type='application/json', data=json.dumps(user))
        response = json.loads(post_request.data.decode())
        self.assertEqual("Password is required", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_password_letters_or_numbers(self):
        user ={
            "user_name" : "dan",
            "password": "#123"
        }
        post_request = self.app_client.post("/api/v1/users", content_type='application/json', data=json.dumps(user))
        response = json.loads(post_request.data.decode())
        self.assertEqual("Password should be letters and/or numbers", response['message'])
        self.assertEqual(post_request.status_code, 400)    
  

if __name__ == ('__main__'):
    unittest.main()