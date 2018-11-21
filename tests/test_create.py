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
    "total_price":2000
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


class Endpoints(Base):
    """
    Tests all aspects of endpoints
    Tests include: creating a parcel delivery order, getting all parcel delivery orders,
    getting a particular parcel delivery order, canceling a parcel delivery order,
    getting all parcel delivery orders by a specific user.  
    """
    def test_admin_create_parcel(self):
        admin_login = self.app_client.post("api/v1/auth/login", content_type="application/json", data=json.dumps({"user_name":"admin", "password":"root"}))
        self.assertEqual(admin_login.status_code, 200)
        response = json.loads(admin_login.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as admin')
        self.admin_access_token = response['access_token']

        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
            data=json.dumps(test_parcel), headers={'Authorization': f"Bearer {self.admin_access_token}"})
        self.assertEqual(post_request.status_code, 200)
        post_response = json.loads(post_request.data.decode())
        self.assertEqual(post_response["message"], "You cannot create parcel delivery orders")

    def test_create_parcel(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"eve", "password":"alg"}))
        self.assertEqual(create_user.status_code, 201)
        
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"eve", "password":"alg"}))
        self.assertEqual(login_user.status_code, 200)
        response = json.loads(login_user.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as eve')
        self.user_access_token = response['access_token']

        response = self.app_client.post("/api/v1/parcels", content_type='application/json', data=json.dumps(test_parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        self.assertEqual(create_user.status_code, 201)
        self.assertEqual(response.status_code, 201)


class Set(Base):
    """
    Tests all aspects of setting attributes
    Tests include: setting attributes of right type, setting attributes of wrong type, 
    setting attributes outside their constraints, setting empty attributes.
    """
    def test_recipient_name_string(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"lydia", "password":"alg"}))
        self.assertEqual(create_user.status_code, 201)
        
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"lydia", "password":"alg"}))
        self.assertEqual(login_user.status_code, 200)
        response = json.loads(login_user.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as lydia')
        self.user_access_token = response['access_token']

        test_parcel.update({"recipient_name": 90})
        post_request = self.app_client.post("/api/v1/parcels",
                                        content_type='application/json',
                                        data=json.dumps(test_parcel),
                                        headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        self.assertIn("Recipient name must be a string", response['errors']['message(s)'][0])
        self.assertEqual(post_request.status_code, 200)

    def test_recipient_name_letters(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"lydia", "password":"alg"}))
        self.assertEqual(create_user.status_code, 201)
        
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"lydia", "password":"alg"}))
        self.assertEqual(login_user.status_code, 200)
        response = json.loads(login_user.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as lydia')
        self.user_access_token = response['access_token']

        test_parcel.update({"recipient_name": "90"})
        post_request = self.app_client.post("/api/v1/parcels",
                                        content_type='application/json',
                                        data=json.dumps(test_parcel),
                                        headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        self.assertIn("Recipient name must be letters", response['errors']['message(s)'][0])
        self.assertEqual(post_request.status_code, 200)

    def test_recipient_name_required(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', 
            data=json.dumps({"user_name":"jj", "password":"alg"}))
        self.assertEqual(create_user.status_code, 201)
        
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', 
            data=json.dumps({"user_name":"jj", "password":"alg"}))
        self.assertEqual(login_user.status_code, 200)
        response = json.loads(login_user.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as jj')
        self.user_access_token = response['access_token']

        test_parcel.update({"recipient_name": ""})
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
            data=json.dumps(test_parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        self.assertIn("Please enter a recipient name", response['errors']['message(s)'][0])
        self.assertEqual(post_request.status_code, 200)

    def test_recipient_mobile_required(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"vinc", "password":"alg"}))
        self.assertEqual(create_user.status_code, 201)
        
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"vinc", "password":"alg"}))
        self.assertEqual(login_user.status_code, 200)
        response = json.loads(login_user.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as vinc')
        self.user_access_token = response['access_token']

        test_parcel.update({"recipient_mobile": ""})
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
            data=json.dumps(test_parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        self.assertIn("Please enter the recipients mobile contact", response['errors']['message(s)'][0])
        self.assertEqual(post_request.status_code, 200)

    def test_recipient_mobile_number(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"james", "password":"alg"}))
        self.assertEqual(create_user.status_code, 201)
        
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"james", "password":"alg"}))
        self.assertEqual(login_user.status_code, 200)
        response = json.loads(login_user.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as james')
        self.user_access_token = response['access_token']

        test_parcel.update({"recipient_mobile": "y"})
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
            data=json.dumps(test_parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        self.assertIn("Recipients mobile contact must be numbers", response['errors']['message(s)'][0])
        self.assertEqual(post_request.status_code, 200)

    def test_recipient_mobile_valid(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"leona", "password":"alg"}))
        self.assertEqual(create_user.status_code, 201)
        
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"leona", "password":"alg"}))
        self.assertEqual(login_user.status_code, 200)
        response = json.loads(login_user.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as leona')
        self.user_access_token = response['access_token']

        test_parcel.update({"recipient_mobile": 100})
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json',
            data=json.dumps(test_parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        self.assertIn("Please enter a valid mobile contact", response['errors']['message(s)'][0])
        self.assertEqual(post_request.status_code, 200)

    def test_pickup_location_required(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"lara", "password":"alg"}))
        self.assertEqual(create_user.status_code, 201)
        
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"lara", "password":"alg"}))
        self.assertEqual(login_user.status_code, 200)
        response = json.loads(login_user.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as lara')
        self.user_access_token = response['access_token']

        test_parcel.update({"pickup_location" : ""})

        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
            data=json.dumps(test_parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        self.assertIn("Please enter a pickup location", response['errors']['message(s)'][0])
        self.assertEqual(post_request.status_code, 200)

    def test_pickup_location_string(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"lara", "password":"alg"}))
        self.assertEqual(create_user.status_code, 201)
        
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"lara", "password":"alg"}))
        self.assertEqual(login_user.status_code, 200)
        response = json.loads(login_user.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as lara')
        self.user_access_token = response['access_token']

        test_parcel.update({"pickup_location" : 99})

        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
            data=json.dumps(test_parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        self.assertIn("Pickup location must be a string", response['errors']['message(s)'][0])
        self.assertEqual(post_request.status_code, 200)


    def test_destination_required(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"mabel", "password":"alg"}))
        self.assertEqual(create_user.status_code, 201)
        
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"mabel", "password":"alg"}))
        self.assertEqual(login_user.status_code, 200)
        response = json.loads(login_user.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as mabel')
        self.user_access_token = response['access_token']

        test_parcel.update({"destination": ""})

        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', data=json.dumps(test_parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        self.assertIn("Please enter a destination", response['errors']['message(s)'][0])
        self.assertEqual(post_request.status_code, 200)

    def test_pickup_location_letters(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"em", "password":"alg"}))
        self.assertEqual(create_user.status_code, 201)
        
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"em", "password":"alg"}))
        self.assertEqual(login_user.status_code, 200)
        response = json.loads(login_user.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as em')
        self.user_access_token = response['access_token']

        test_parcel.update({"pickup_location" : "90"})

        post_request = self.app_client.post("/api/v1/parcels",
                                        content_type='application/json',
                                        data=json.dumps(test_parcel),
                                        headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        self.assertIn("Pickup location must be letters", response['errors']['message(s)'][0])
        self.assertEqual(post_request.status_code, 200)

    def test_destination_letters(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"mary", "password":"alg"}))
        self.assertEqual(create_user.status_code, 201)
        
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"mary", "password":"alg"}))
        self.assertEqual(login_user.status_code, 200)
        response = json.loads(login_user.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as mary')
        self.user_access_token = response['access_token']

        test_parcel.update({"destination": "89"})

        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', data=json.dumps(test_parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        self.assertIn("Destination must be letters", response['errors']['message(s)'][0])
        self.assertEqual(post_request.status_code, 200)

    def test_destination_string(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"mary", "password":"alg"}))
        self.assertEqual(create_user.status_code, 201)
        
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"mary", "password":"alg"}))
        self.assertEqual(login_user.status_code, 200)
        response = json.loads(login_user.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as mary')
        self.user_access_token = response['access_token']

        test_parcel.update({"destination": 89})

        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', data=json.dumps(test_parcel), headers={'Authorization':f"Bearer {self.user_access_token}"})
        response = json.loads(post_request.data.decode())
        self.assertIn("Destination must be a string", response['errors']['message(s)'][0])
        self.assertEqual(post_request.status_code, 200)
   

    
    

    


if __name__ == ('__main__'):
    unittest.main()