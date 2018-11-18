import json
import unittest
from app import app
from app.routes.parcel_routes import *
from app.routes.user_routes import *

test_user ={
    "user_name" : "lynn",
	"password": "alg"
}

test_parcel = {
    "recipient_name": "Corn",
    "recipient_mobile": 1234567890,
    "pickup_location" : "Kampala",
    "destination": "Namugongo",
    "items": [{"item_name": "Shoes", "item_weight": 40}]
}

class Base(unittest.TestCase):
    """Base class for tests. 
    This class defines a common `setUp` 
    method that defines attributes which 
    are used in the various tests.
    """

    def setUp(self):
        self.app_client = app.test_client()


# class Endpoints(Base):
#     """
#     Tests all aspects of endpoints
#     Tests include: creating a parcel delivery order, getting all parcel delivery orders,
#     getting a particular parcel delivery order, canceling a parcel delivery order,
#     getting all parcel delivery orders by a specific user.  
#     """
#     def test_non_user_create_parcel(self):
#         create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"john", "password":"alg"}))
#         self.assertEqual(create_user.status_code, 201)
        
#         login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"john", "password":"alg"}))
#         self.assertEqual(login_user.status_code, 200)
#         response = json.loads(login_user.data.decode())
#         self.assertEqual(response['message'], 'You have successfully been logged in as john')
#         self.user_access_token = response['access_token']

#         parcel = {
#             "user_id":100,
#             "recipient_name": "Corn",
#             "recipient_mobile": 1234567890,
#             "pickup_location" : "Kampala",
#             "destination": "Namugongo",
#             "items": [{"item_name": "Shoes", "item_weight": 40}]
#         }
#         post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', data=json.dumps(parcel))
#         self.assertEqual(response.status_code, 200)
#         response = json.loads(post_request.data.decode())
#         self.assertEqual(reponse["message"], "You dont have rights to create a parcel delivery order")


#     def test_non_user_create_parcel(self):
#         create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"john", "password":"alg"}))
#         self.assertEqual(create_user.status_code, 201)
        
#         login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"john", "password":"alg"}))
#         self.assertEqual(login_user.status_code, 200)
#         response = json.loads(login_user.data.decode())
#         self.assertEqual(response['message'], 'You have successfully been logged in as john')
#         self.user_access_token = response['access_token']

#         # create_user = self.app_client.post("/api/v1/users", content_type='application/json', data=json.dumps(user))
#         response = self.app_client.post("/api/v1/parcels", content_type='application/json', data=json.dumps(test_parcel))
#         # self.assertEqual(create_user.status_code, 201)
#         self.assertEqual(response.status_code, 201)


class Set(Base):
    """
    Tests all aspects of setting attributes
    Tests include: setting attributes of right type, setting attributes of wrong type, 
    setting attributes outside their constraints, setting empty attributes.
    """
    def test_create_parcel(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"eve", "password":"alg"}))
        self.assertEqual(create_user.status_code, 201)
        
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"eve", "password":"alg"}))
        self.assertEqual(login_user.status_code, 200)
        response = json.loads(login_user.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as eve')
        self.user_access_token = response['access_token']

        response = self.app_client.post("/api/v1/parcels", content_type='application/json', data=json.dumps(test_parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        # self.assertEqual(create_user.status_code, 201)
        self.assertEqual(response.status_code, 201)

    def test_recipient_name_letters(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"lydia", "password":"alg"}))
        self.assertEqual(create_user.status_code, 201)
        
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"lydia", "password":"alg"}))
        self.assertEqual(login_user.status_code, 200)
        response = json.loads(login_user.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as lydia')
        self.user_access_token = response['access_token']

        parcel = {
                "user_id" : 1,
                "recipient_name": "90",
                "recipient_mobile": 1234567890,
                "pickup_location" : "Kampala",
                "destination": "Namugongo",
                "items": [{"item_name": "Shoes", "item_weight": 40, }]
        }
        post_request = self.app_client.post("/api/v1/parcels",
                                        content_type='application/json',
                                        data=json.dumps(parcel),
                                        headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        # self.assertIn("Recipient name must be letters", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_recipient_name_required(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"jj", "password":"alg"}))
        self.assertEqual(create_user.status_code, 201)
        
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"jj", "password":"alg"}))
        self.assertEqual(login_user.status_code, 200)
        response = json.loads(login_user.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as jj')
        self.user_access_token = response['access_token']

        parcel = {
            "user_id" : 1,
            "recipient_name": "",
            "recipient_mobile": 1234567890,
            "pickup_location" : "Kampala",
            "destination": "Namugongo",
            "items": [{"item_name": "Shoes", "item_weight": 40}]
        }
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', data=json.dumps(parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        # self.assertIn("Recipient name is required", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_recipient_mobile_required(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"vinc", "password":"alg"}))
        self.assertEqual(create_user.status_code, 201)
        
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"vinc", "password":"alg"}))
        self.assertEqual(login_user.status_code, 200)
        response = json.loads(login_user.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as vinc')
        self.user_access_token = response['access_token']

        parcel = {
            "recipient_name": "Corn",
            "recipient_mobile": "",
            "pickup_location" : "Kampala",
            "destination": "Namugongo",
            "items": [{"item_name": "Shoes", "item_weight": 40}]
        }
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', data=json.dumps(parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        # self.assertIn("Recipient mobile contact is required", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_recipient_mobile_number(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"james", "password":"alg"}))
        self.assertEqual(create_user.status_code, 201)
        
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"james", "password":"alg"}))
        self.assertEqual(login_user.status_code, 200)
        response = json.loads(login_user.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as james')
        self.user_access_token = response['access_token']

        parcel = {
            "recipient_name": "Corn",
            "recipient_mobile": "y",
            "pickup_location" : "Kampala",
            "destination": "Namugongo",
            "items": [{"item_name": "Shoes", "item_weight": 40}]
        }
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', data=json.dumps(parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        # self.assertIn("Recipient mobile contact must be numbers", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_recipient_mobile_valid(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"leona", "password":"alg"}))
        self.assertEqual(create_user.status_code, 201)
        
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"leona", "password":"alg"}))
        self.assertEqual(login_user.status_code, 200)
        response = json.loads(login_user.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as leona')
        self.user_access_token = response['access_token']

        parcel = {
            "recipient_name": "Corn",
            "recipient_mobile": 100,
            "pickup_location" : "Kampala",
            "destination": "Namugongo",
            "items": [{"item_name": "Shoes", "item_weight": 40}]
        }
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', data=json.dumps(parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        # self.assertIn("Please enter a valid mobile contact", response['message'])
        # self.assertEqual(post_request.status_code, 400)

    def test_pickup_location_required(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"lara", "password":"alg"}))
        self.assertEqual(create_user.status_code, 201)
        
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"lara", "password":"alg"}))
        self.assertEqual(login_user.status_code, 200)
        response = json.loads(login_user.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as lara')
        self.user_access_token = response['access_token']

        parcel = {
            "recipient_name": "Corn",
            "recipient_mobile": 1234567890,
            "pickup_location" : "",
            "destination": "Namugongo",
            "items": [{"item_name": "Shoes", "item_weight": 40}]
        }
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', data=json.dumps(parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        # self.assertIn("Pickup location is required", response['message'])
        self.assertEqual(post_request.status_code, 400)


    def test_destination_required(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"mabel", "password":"alg"}))
        self.assertEqual(create_user.status_code, 201)
        
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"mabel", "password":"alg"}))
        self.assertEqual(login_user.status_code, 200)
        response = json.loads(login_user.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as mabel')
        self.user_access_token = response['access_token']

        parcel = {
            "recipient_name": "Corn",
            "recipient_mobile": 1234567890,
            "pickup_location" : "Kampala",
            "destination": "",
            "items": [{"item_name": "Shoes", "item_weight": 40}]
        }
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', data=json.dumps(parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        # self.assertIn("Destination is required", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_pickup_location_letters(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"em", "password":"alg"}))
        self.assertEqual(create_user.status_code, 201)
        
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"em", "password":"alg"}))
        self.assertEqual(login_user.status_code, 200)
        response = json.loads(login_user.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as em')
        self.user_access_token = response['access_token']

        parcel = {
            "recipient_name": "Corn",
            "recipient_mobile": 1234567890,
            "pickup_location" : "90",
            "destination": "Namugongo",
            "items": [{"item_name": "Shoes", "item_weight": 40}]
        }
        post_request = self.app_client.post("/api/v1/parcels",
                                        content_type='application/json',
                                        data=json.dumps(parcel),
                                        headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        # self.assertIn("Pickup location must be letters", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_destination_letters(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"mary", "password":"alg"}))
        self.assertEqual(create_user.status_code, 201)
        
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"mary", "password":"alg"}))
        self.assertEqual(login_user.status_code, 200)
        response = json.loads(login_user.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as mary')
        self.user_access_token = response['access_token']

        parcel = {
            "recipient_name": "Corn",
            "recipient_mobile": 1234567890,
            "pickup_location" : "Kampala",
            "destination": "89",
            "items": [{"item_name": "Shoes", "item_weight": 40}]
        }
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', data=json.dumps(parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        # self.assertIn("Destination must be letters", response['message'])
        self.assertEqual(post_request.status_code, 400)
   

    def test_parcel_items_required(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"rick", "password":"alg"}))
        self.assertEqual(create_user.status_code, 201)
        
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"rick", "password":"alg"}))
        self.assertEqual(login_user.status_code, 200)
        response = json.loads(login_user.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as rick')
        self.user_access_token = response['access_token']
        parcel = {
            "recipient_name": "Corn",
            "recipient_mobile": 1234567890,
            "pickup_location" : "Kampala",
            "destination": "Namugongo",
            "items": ""
        }
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', data=json.dumps(parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        # self.assertIn("Please enter atleast one item; Items must be a list of dictionaries", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_parcel_items_list(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"mercy", "password":"alg"}))
        self.assertEqual(create_user.status_code, 201)
        
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"mercy", "password":"alg"}))
        self.assertEqual(login_user.status_code, 200)
        response = json.loads(login_user.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as mercy')
        self.user_access_token = response['access_token']

        parcel = {
            "recipient_name": "Corn",
            "recipient_mobile": 1234567890,
            "pickup_location" : "Kampala",
            "destination": "Namugongo",
            "items": "cook"
        }
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', data=json.dumps(parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        # self.assertIn("Please enter atleast one item; Items must be a list of dictionaries", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_parcel_itemname_required(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"john", "password":"alg"}))
        self.assertEqual(create_user.status_code, 201)
        
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"john", "password":"alg"}))
        self.assertEqual(login_user.status_code, 200)
        response = json.loads(login_user.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as john')
        self.user_access_token = response['access_token']

        parcel = {
                "recipient_name": "Corn",
                "recipient_mobile": 1234567890,
                "pickup_location" : "Kampala",
                "destination": "Namugongo",
                "items": [{"item_name": "", "item_weight": 40}]
        }
        post_request = self.app_client.post("/api/v1/parcels",
                                        content_type='application/json',
                                        data=json.dumps(parcel),
                                        headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        # self.assertIn("Parcel item name is required", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_itemname_letters(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"becky", "password":"alg"}))
        self.assertEqual(create_user.status_code, 201)
        
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"becky", "password":"alg"}))
        self.assertEqual(login_user.status_code, 200)
        response = json.loads(login_user.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as becky')
        self.user_access_token = response['access_token']

        parcel = {
                "recipient_name": "Corn",
                "recipient_mobile": 1000000000,
                "pickup_location" : "Kampala",
                "destination": "Namugongo",
                "items": [{"item_name": "22", "item_weight": 40}]
        }
        post_request = self.app_client.post("/api/v1/parcels",content_type='application/json',data=json.dumps(parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        # self.assertIn("Parcel item name must be letters", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_itemweight_required(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"clerk", "password":"alg"}))
        self.assertEqual(create_user.status_code, 201)
        
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"clerk", "password":"alg"}))
        self.assertEqual(login_user.status_code, 200)
        response = json.loads(login_user.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as clerk')
        self.user_access_token = response['access_token']

        parcel = {
                "recipient_name": "Corn",
                "recipient_mobile": 1000000000,
                "pickup_location" : "Kampala",
                "destination": "Namugongo",
                "items": [{"item_name": "Shoes", "item_weight": ""}]
        }
        post_request = self.app_client.post("/api/v1/parcels",
                                        content_type='application/json',
                                        data=json.dumps(parcel),
                                        headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        # self.assertIn("Parcel item weight is required", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_itemweight_number(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps(test_user))
        self.assertEqual(create_user.status_code, 201)
        
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"lynn", "password":"alg"}))
        self.assertEqual(login_user.status_code, 200)
        response = json.loads(login_user.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as lynn')
        self.user_access_token = response['access_token']

        parcel = {
            "recipient_name": "Corn",
            "recipient_mobile": 1234567890,
            "pickup_location" : "Kampala",
            "destination": "Namugongo",
            "items": [{"item_name": "Shoes", "item_weight": "x"}]
        }
        post_request = self.app_client.post("/api/v1/parcels",
                                        content_type='application/json',
                                        data=json.dumps(parcel),
                                        headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        # self.assertIn("Parcel item weight must be an integer", response['message'])
        self.assertEqual(post_request.status_code, 400)

    

    


if __name__ == ('__main__'):
    unittest.main()