import json
import unittest
from app import app
from app.routes.parcel_routes import *
from app.routes.user_routes import *
from app.controllers.db import DatabaseConnection

test_user ={
    "user_name" : "lynn",
	"password": "alg"
}

test_parcel = {
    "recipient_name" : "cara",
    "recipient_mobile": 1234567890,
    "pickup_location" : "gulu",
    "destination": "kampala",
    "weight":200,
}

db = DatabaseConnection()

class Base(unittest.TestCase):
    """Base class for tests. 
    This class defines a common `setUp` 
    method that defines attributes which 
    are used in the various tests.
    """

    def setUp(self):
        self.app_client = app.test_client()
        db.setUp()

    def tearDown(self):
        db.delete_tables()

    def admin_login(self):
        admin_login = self.app_client.post("api/v1/auth/login", content_type="application/json", data=json.dumps({"user_name":"admin", "password":"root"}))
        self.assertEqual(admin_login.status_code, 200)
        response = json.loads(admin_login.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as admin')
        self.admin_access_token = response['access_token']

    def sign_up(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"eve", "password":"alg"}))
        self.assertEqual(create_user.status_code, 201)

    def user_login(self):
        self.sign_up()
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"eve", "password":"alg"}))
        self.assertEqual(login_user.status_code, 200)
        response = json.loads(login_user.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as eve')
        self.user_access_token = response['access_token']

    def sign_up_user2(self):
        create_user2 = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"harriet", "password":"sleeve"}))
        self.assertEqual(create_user2.status_code, 201)

    def user2_login(self):
        self.sign_up_user2()
        login_user2 = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"harriet", "password":"sleeve"}))
        self.assertEqual(login_user2.status_code, 200)
        response2 = json.loads(login_user2.data.decode())
        self.assertEqual(response2['message'], 'You have successfully been logged in as harriet')
        self.user_access_token2 = response2['access_token']

class Endpoints(Base):
    """
    Tests all aspects of endpoints
    Tests include: creating a parcel delivery order, getting all parcel delivery orders,
    getting a particular parcel delivery order, canceling a parcel delivery order,
    getting all parcel delivery orders by a specific user.  
    """
    def test_admin_create_parcel(self):
        self.admin_login()

        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
            data=json.dumps(test_parcel), headers={'Authorization': f"Bearer {self.admin_access_token}"})
        self.assertEqual(post_request.status_code, 200)
        post_response = json.loads(post_request.data.decode())
        self.assertEqual(post_response["message"], "You cannot create parcel delivery orders")

    def test_create_parcel(self):
        self.user_login()

        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', data=json.dumps(test_parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        self.assertEqual(post_request.status_code, 201)
        response = json.loads(post_request.data.decode())
        self.assertEqual(response['message'], 'Parcel successfully created')
        


class Set(Base):
    """
    Tests all aspects of setting attributes
    Tests include: setting attributes of right type, setting attributes of wrong type, 
    setting attributes outside their constraints, setting empty attributes.
    """
    def test_recipient_name_string(self):
        self.user_login()

        test_parcel = {
            "recipient_name" : 90,
            "recipient_mobile": 1234567890,
            "pickup_location" : "gulu",
            "destination": "kampala",
            "weight":200,
        }
        post_request = self.app_client.post("/api/v1/parcels",
                                        content_type='application/json',
                                        data=json.dumps(test_parcel),
                                        headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        self.assertIn("recipient_name must be a string", response['message(s)'][0])
        self.assertEqual(post_request.status_code, 400)

    def test_recipient_name_letters(self):
        self.user_login()

        test_parcel = {
            "recipient_name" : "2",
            "recipient_mobile": 1234567890,
            "pickup_location" : "gulu",
            "destination": "kampala",
            "weight":200,
        }
        post_request = self.app_client.post("/api/v1/parcels",
                                        content_type='application/json',
                                        data=json.dumps(test_parcel),
                                        headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        self.assertIn("recipient_name must be letters", response['message(s)'][0])
        self.assertEqual(post_request.status_code, 400)

    def test_recipient_name_required(self):
        self.user_login()

        test_parcel = {
            "recipient_name" : "",
            "recipient_mobile": 1234567890,
            "pickup_location" : "gulu",
            "destination": "kampala",
            "weight":200,
        }
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
            data=json.dumps(test_parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        self.assertIn("Please enter the recipient_name", response['message(s)'][0])
        self.assertEqual(post_request.status_code, 400)

    def test_recipient_mobile_required(self):
        self.user_login()

        test_parcel = {
            "recipient_name" : "cara",
            "recipient_mobile": "",
            "pickup_location" : "gulu",
            "destination": "kampala",
            "weight":200,
        }

        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
            data=json.dumps(test_parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        self.assertIn("Please enter the recipient_mobile", response['message(s)'][0])
        self.assertEqual(post_request.status_code, 400)

    def test_recipient_mobile_number(self):
        self.user_login()

        test_parcel = {
            "recipient_name" : "cara",
            "recipient_mobile": "pill",
            "pickup_location" : "gulu",
            "destination": "kampala",
            "weight":200,
        }
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
            data=json.dumps(test_parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        self.assertIn("recipient_mobile must be numbers", response['message(s)'][0])
        self.assertEqual(post_request.status_code, 400)

    def test_recipient_mobile_valid(self):
        self.user_login()

        test_parcel = {
            "recipient_name" : "cara",
            "recipient_mobile": 1,
            "pickup_location" : "gulu",
            "destination": "kampala",
            "weight":200,
        }
        
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json',
            data=json.dumps(test_parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        self.assertIn("Please enter a valid mobile contact", response['message(s)'][0])
        self.assertEqual(post_request.status_code, 400)

    def test_pickup_location_required(self):
        self.user_login()

        test_parcel = {
            "recipient_name" : "cara",
            "recipient_mobile": 1234567890,
            "pickup_location" : "",
            "destination": "kampala",
            "weight":200,
        }

        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
            data=json.dumps(test_parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        self.assertIn("Please enter the pickup_location", response['message(s)'][0])
        self.assertEqual(post_request.status_code, 400)

    def test_pickup_location_string(self):
        self.user_login()

        test_parcel = {
            "recipient_name" : "cara",
            "recipient_mobile": 1234567890,
            "pickup_location" : 2,
            "destination": "kampala",
            "weight":200,
        }

        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
            data=json.dumps(test_parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        self.assertIn("pickup_location must be a string", response['message(s)'][0])
        self.assertEqual(post_request.status_code, 400)


    def test_destination_required(self):
        self.user_login()

        test_parcel = {
            "recipient_name" : "cara",
            "recipient_mobile": 1234567890,
            "pickup_location" : "gulu",
            "destination": "",
            "weight":200,
        }

        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', data=json.dumps(test_parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        self.assertIn("Please enter the destination", response['message(s)'][0])
        self.assertEqual(post_request.status_code, 400)

    def test_pickup_location_letters(self):
        self.user_login()

        test_parcel = {
            "recipient_name" : "cara",
            "recipient_mobile": 1234567890,
            "pickup_location" : "2",
            "destination": "kampala",
            "weight":200,
        }
        post_request = self.app_client.post("/api/v1/parcels",
                                        content_type='application/json',
                                        data=json.dumps(test_parcel),
                                        headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        self.assertIn("pickup_location must be letters", response['message(s)'][0])
        self.assertEqual(post_request.status_code, 400)

    def test_destination_letters(self):
        self.user_login()

        test_parcel = {
            "recipient_name" : "cara",
            "recipient_mobile": 1234567890,
            "pickup_location" : "gulu",
            "destination": "6",
            "weight":200,
        }

        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', data=json.dumps(test_parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        self.assertIn("destination must be letters", response['message(s)'][0])
        self.assertEqual(post_request.status_code, 400)

    def test_destination_string(self):
        self.user_login()

        test_parcel = {
            "recipient_name" : "cara",
            "recipient_mobile": 1234567890,
            "pickup_location" : "gulu",
            "destination": 7,
            "weight":200,
        }

        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', data=json.dumps(test_parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        self.assertIn("destination must be a string", response['message(s)'][0])
        self.assertEqual(post_request.status_code, 400)
   

    def test_weight_required(self):
        self.user_login()

        test_parcel = {
            "recipient_name" : "cara",
            "recipient_mobile": 1234567890,
            "pickup_location" : "gulu",
            "destination": "kampala",
            "weight":"",
        }

        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
            data=json.dumps(test_parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        self.assertIn("Please enter the weight", response['message(s)'][0])
        self.assertEqual(post_request.status_code, 400)

    def test_weight_number(self):
        self.user_login()
        test_parcel = {
            "recipient_name" : "cara",
            "recipient_mobile": 1234567890,
            "pickup_location" : "gulu",
            "destination": "kampala",
            "weight":"clap",
        }
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
            data=json.dumps(test_parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        self.assertIn("weight must be numbers", response['message(s)'][0])
        self.assertEqual(post_request.status_code, 400)

if __name__ == ('__main__'):
    unittest.main()