import json
import unittest
from app import app
from app.routes.parcel_routes import *
from app.routes.user_routes import *
from app.controllers.db import DatabaseConnection

test_user ={
    "user_name" : "eve",
    "user_email" : "eve@gmail.com",
    "user_mobile" : "0777777777",
	"user_password": "algorithm"
}

test_user2 ={
    "user_name" : "maria",
    "user_email" : "maria@gmail.com",
    "user_mobile" : "0777777777",
	"user_password": "algorithm"
}

test_parcel = {
    "description" : "Electronics",
    "recipient_name" : "cara",
    "recipient_mobile": "0777777999",
    "pickup_location" : "Nakawa, Uganda",
    "destination": "Kampala, Uganda",
    "weight":200,
}

db = DatabaseConnection()

class Base(unittest.TestCase):
    """Base class for tests. 
    This class defines a common `setUp` method that defines attributes which 
    are used in the various tests.
    """

    def setUp(self):
        self.app_client = app.test_client()
        db.setUp()

    def tearDown(self):
        db.delete_tables()

    def admin_login(self):
        admin_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
            data=json.dumps({"user_name":"admin", "user_password":"rootsroot"}))
        self.assertEqual(admin_login.status_code, 200)
        response = json.loads(admin_login.data)
        self.assertEqual(response['success'], 'You have successfully been logged in as admin')
        self.admin_access_token = response['access_token']

    def sign_up(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', 
            data=json.dumps(test_user))
        self.assertEqual(create_user.status_code, 201)
        response = json.loads(create_user.data)
        self.assertEqual(response['message'], 'User eve successfully created')

    def user_login(self):
        self.sign_up()
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', 
            data=json.dumps({"user_name":"eve", "user_password":"algorithm"}))
        self.assertEqual(login_user.status_code, 200)
        response = json.loads(login_user.data)
        self.assertEqual(response['success'], 'You have successfully been logged in as eve')
        self.user_access_token = response['access_token']

    def sign_up_user2(self):
        create_user2 = self.app_client.post("/api/v1/auth/signup", content_type='application/json', 
            data=json.dumps(test_user2))
        self.assertEqual(create_user2.status_code, 201)
        response = json.loads(create_user2.data)
        self.assertEqual(response['message'], 'User maria successfully created')

    def user2_login(self):
        self.sign_up_user2()
        login_user2 = self.app_client.post('/api/v1/auth/login', content_type='application/json', 
            data=json.dumps({"user_name":"maria", "user_password":"algorithm"}))
        self.assertEqual(login_user2.status_code, 200)
        response2 = json.loads(login_user2.data)
        self.assertEqual(response2['success'], 'You have successfully been logged in as maria')
        self.user_access_token2 = response2['access_token']

class Endpoints(Base):
    """
    Tests all aspects of the create parcel endpoint
    Tests include: creating a parcel delivery order.  
    """
    def test_create_parcel(self):
        self.user_login()
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', data=json.dumps(test_parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        self.assertEqual(post_request.status_code, 201)
        response = json.loads(post_request.data)
        self.assertEqual(response['message'], 'Parcel delivery order successfully made')
        

class Set(Base):
    """
    Tests all aspects of setting attributes
    Tests include: setting attributes of wrong type, 
    setting attributes outside their constraints, setting empty attributes.
    """
    def test_description_required(self):
        self.user_login()
        test_parcel = {
            "recipient_name" : "cara",
            "recipient_mobile": "0777777999",
            "pickup_location" : "Nakawa, Uganda",
            "destination": "Kampala, Uganda",
            "weight":200
        }
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
            data=json.dumps(test_parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data)
        self.assertIn("Please enter the description", response['message'][0])
        self.assertEqual(post_request.status_code, 400)

    def test_description_letters(self):
        self.user_login()
        test_parcel = {
            "description" : "90",
            "recipient_name" : "cara",
            "recipient_mobile": "0777777999",
            "pickup_location" : "Nakawa, Uganda",
            "destination": "Kampala, Uganda",
            "weight":200
        }
        post_request = self.app_client.post("/api/v1/parcels",
                                        content_type='application/json',
                                        data=json.dumps(test_parcel),
                                        headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data)
        self.assertIn("description must be letters", response['message'][0])
        self.assertEqual(post_request.status_code, 400)


    def test_recipient_name_letters(self):
        self.user_login()
        test_parcel = {
            "description" : "Electronics",
            "recipient_name" : "2",
            "recipient_mobile": "0777777999",
            "pickup_location" : "Nakawa, Uganda",
            "destination": "Kampala, Uganda",
            "weight":200,
        }
        post_request = self.app_client.post("/api/v1/parcels",
                                        content_type='application/json',
                                        data=json.dumps(test_parcel),
                                        headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data)
        self.assertIn("recipient_name must be letters", response['message'][0])
        self.assertEqual(post_request.status_code, 400)

    def test_recipient_name_required(self):
        self.user_login()
        test_parcel = {
            "description" : "Electronics",
            # "recipient_name" : "",
            "recipient_mobile": "0777777999",
            "pickup_location" : "Nakawa, Uganda",
            "destination": "Kampala, Uganda",
            "weight":200
        }
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
            data=json.dumps(test_parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data)
        self.assertIn("Please enter the recipient_name", response['message'][0])
        self.assertEqual(post_request.status_code, 400)

    # def test_recipient_mobile_required(self):
    #     self.user_login()
    #     test_parcel = {
    #         "description" : "Electronics",
    #         "recipient_name" : "cara",
    #         # "recipient_mobile": "",
    #         "pickup_location" : "Nakawa, Uganda",
    #         "destination": "Kampala, Uganda",
    #         "weight":200
    #     }

    #     post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
    #         data=json.dumps(test_parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
    #     response = json.loads(post_request.data)
    #     self.assertIn("Please enter the recipient_mobile", response['message'][0])
    #     self.assertEqual(post_request.status_code, 400)

    # def test_recipient_mobile_number(self):
    #     self.user_login()
    #     test_parcel = {
    #         "description" : "Electronics",
    #         "recipient_name" : "cara",
    #         "recipient_mobile": "pill",
    #         "pickup_location" : "Nakawa, Uganda",
    #         "destination": "Kampala, Uganda",
    #         "weight":200
    #     }
    #     post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
    #         data=json.dumps(test_parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
    #     response = json.loads(post_request.data)
    #     self.assertIn("recipient_mobile must be numbers", response['message'][0])
    #     self.assertEqual(post_request.status_code, 400)

    def test_recipient_mobile_valid(self):
        self.user_login()
        test_parcel = {
            "description" : "Electronics",
            "recipient_name" : "cara",
            "recipient_mobile": "1",
            "pickup_location" : "Nakawa, Uganda",
            "destination": "Kampala, Uganda",
            "weight":200
        }   
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json',
            data=json.dumps(test_parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data)
        self.assertIn("Please enter a valid mobile contact", response['message'][0])
        self.assertEqual(post_request.status_code, 400)

    def test_pickup_location_required(self):
        self.user_login()
        test_parcel = {
            "description" : "Electronics",
            "recipient_name" : "cara",
            "recipient_mobile": "0777777999",
            # "pickup_location" : "",
            "destination": "Kampala, Uganda",
            "weight":200
        }
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
            data=json.dumps(test_parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data)
        self.assertIn("Please enter the pickup_location", response['message'][0])
        self.assertEqual(post_request.status_code, 400)

    def test_destination_required(self):
        self.user_login()
        test_parcel = {
            "description" : "Electronics",
            "recipient_name" : "cara",
            "recipient_mobile": "0777777999",
            "pickup_location" : "Nakawa, Uganda",
            # "destination": "",
            "weight":200
        }
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', data=json.dumps(test_parcel), 
            headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data)
        self.assertIn("Please enter the destination", response['message'][0])
        self.assertEqual(post_request.status_code, 400)

    def test_pickup_location_letters(self):
        self.user_login()
        test_parcel = {
            "description" : "Electronics",
            "recipient_name" : "cara",
            "recipient_mobile": "0777777999",
            "pickup_location" : "90",
            "destination": "Kampala, Uganda",
            "weight":200
        }
        post_request = self.app_client.post("/api/v1/parcels",
                                        content_type='application/json',
                                        data=json.dumps(test_parcel),
                                        headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data)
        self.assertIn("pickup_location must be letters", response['message'][0])
        self.assertEqual(post_request.status_code, 400)

    def test_destination_letters(self):
        self.user_login()
        test_parcel = {
            "description" : "Electronics",
            "recipient_name" : "cara",
            "recipient_mobile": "0777777999",
            "pickup_location" : "Nakawa, Uganda",
            "destination": "00",
            "weight":200
        }
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
            data=json.dumps(test_parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data)
        self.assertIn("destination must be letters", response['message'][0])
        self.assertEqual(post_request.status_code, 400)

    # def test_weight_required(self):
    #     self.user_login()
    #     test_parcel = {
    #         "description" : "Electronics",
    #         "recipient_name" : "cara",
    #         "recipient_mobile": "0777777999",
    #         "pickup_location" : "Nakawa, Uganda",
    #         "destination": "Kampala, Uganda"
    #         # "weight":""
    #     }
    #     post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
    #         data=json.dumps(test_parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
    #     response = json.loads(post_request.data)
    #     self.assertIn("Please enter the weight", response['message'][0])
    #     self.assertEqual(post_request.status_code, 400)

    def test_weight_number(self):
        self.user_login()
        test_parcel = {
            "description" : "Electronics",
            "recipient_name" : "cara",
            "recipient_mobile": "0777777999",
            "pickup_location" : "Nakawa, Uganda",
            "destination": "Kampala, Uganda",
            "weight":"Cara"
        }
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
            data=json.dumps(test_parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data)
        self.assertIn("Weight must be a number", response['message'][0])
        self.assertEqual(post_request.status_code, 400)

if __name__ == ('__main__'):
    unittest.main()