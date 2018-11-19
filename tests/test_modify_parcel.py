import json
import unittest
from app import app
from app.routes.parcel_routes import *
from app.routes.user_routes import *

test_user ={
    "user_name" : "andrew",
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

        # create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps(test_user))
        # self.assertEqual(create_user.status_code, 201)
        
        # login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"andrew", "password":"alg"}))
        # self.assertEqual(login_user.status_code, 200)
        # response = json.loads(login_user.data.decode())
        # self.assertEqual(response['message'], 'You have successfully been logged in as andrew')
        # self.user_access_token = response['access_token']
        
        # admin_login = self.app_client.post("api/v1/auth/login", content_type="application/json", data=json.dumps({"user_name":"admin", "password":"root"}))
        # self.assertEqual(admin_login.status_code, 200)
        # response = json.loads(admin_login.data.decode())
        # self.assertEqual(response['message'], 'You have been logged in as admin')
        # self.admin_access_token = response['access_token']


class Endpoints(Base):
    """
    Tests all aspects of endpoints
    Tests include: canceling a parcel delivery order.  
    """

    def test_change_present_location(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps(test_user))
        self.assertEqual(create_user.status_code, 201)
        
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"andrew", "password":"alg"}))
        self.assertEqual(login_user.status_code, 200)
        response = json.loads(login_user.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as andrew')
        self.user_access_token = response['access_token']
        
        admin_login = self.app_client.post("api/v1/auth/login", content_type="application/json", data=json.dumps({"user_name":"admin", "password":"root"}))
        self.assertEqual(admin_login.status_code, 200)
        response = json.loads(admin_login.data.decode())
        self.assertEqual(response['message'], 'You have been logged in as admin')
        self.admin_access_token = response['access_token']

        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', headers={'Authorization': f"Bearer {self.user_access_token}"}, data=json.dumps(test_parcel))
        put_request = self.app_client.put("/api/v1/parcels/1/present_location", content_type='application/json', data=json.dumps({"present_location":"masaka"}), headers={'Authorization': f"Bearer {self.admin_access_token}"})
        self.assertEqual(post_request.status_code, 201)
        self.assertEqual(put_request.status_code, 200)

    # def test_change_destination(self):
    #     create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"joel", "password":"alg"}))
    #     self.assertEqual(create_user.status_code, 201)
        
    #     login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"joel", "password":"alg"}))
    #     self.assertEqual(login_user.status_code, 200)
    #     response = json.loads(login_user.data.decode())
    #     self.assertEqual(response['message'], 'You have successfully been logged in as joel')
    #     self.user_access_token = response['access_token']
 
    #     post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', headers={'Authorization': f"Bearer {self.user_access_token}"}, data=json.dumps(test_parcel))
    #     put_request = self.app_client.put("/api/v1/parcels/1/destination", content_type='application/json', data=json.dumps({"destination":"masaka"}), headers={'Authorization': f"Bearer {self.user_access_token}"})
    #     self.assertEqual(post_request.status_code, 201)
    #     self.assertEqual(put_request.status_code, 200)

class Set(Base):
    """
    Tests all aspects of setting attributes
    Tests include: canceling a non-existent parcel delivery order, non-admin canceling a parcel delivery order.
    """

    def test_change_present_location_non_existent_parcel_delivery_order(self):       
        admin_login = self.app_client.post("api/v1/auth/login", content_type="application/json", data=json.dumps({"user_name":"admin", "password":"root"}))
        self.assertEqual(admin_login.status_code, 200)
        response = json.loads(admin_login.data.decode())
        self.assertEqual(response['message'], 'You have been logged in as admin')
        self.admin_access_token = response['access_token']

        put_request = self.app_client.put("/api/v1/parcels/100/present_location", data=json.dumps({"present_location":"masaka"}), headers={'Authorization': f"Bearer {self.admin_access_token}"})
        response = json.loads(put_request.data.decode())
        self.assertEqual(put_request.status_code, 200)
        self.assertEqual(response['message'], "There is no parcel with that ID")

    # def test_change_destination_non_existent_parcel_delivery_order(self):       
    #     create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"momo", "password":"alg"}))
    #     self.assertEqual(create_user.status_code, 201)
        
    #     login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"momo", "password":"alg"}))
    #     self.assertEqual(login_user.status_code, 200)
    #     response = json.loads(login_user.data.decode())
    #     self.assertEqual(response['message'], 'You have successfully been logged in as momo')
    #     self.user_access_token = response['access_token']

    #     put_request = self.app_client.put("/api/v1/parcels/100/destination", data=json.dumps({"destination":"masaka"}), headers={'Authorization': f"Bearer {self.user_access_token}"})
    #     response = json.loads(put_request.data.decode())
    #     # self.assertEqual(put_request.status_code, 200)
    #     self.assertEqual(response['message'], "There is no parcel with that ID")


    def test_wrong_user_change_pickup_location(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"myriam", "password":"sleeve"}))
        self.assertEqual(create_user.status_code, 201)
        
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"myriam", "password":"sleeve"}))
        self.assertEqual(login_user.status_code, 200)
        response = json.loads(login_user.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as myriam')
        self.user_access_token = response['access_token']

        put_request = self.app_client.put("/api/v1/parcels/1/present_location", data=json.dumps({"present_location":"masaka"}), headers={'Authorization': f"Bearer {self.user_access_token}"})
        response = json.loads(put_request.data.decode())
        self.assertEqual(put_request.status_code, 400)
        self.assertEqual(response['message'], "Invalid request! login or use the right access token")

    def test_wrong_user_change_destination(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"ryan", "password":"sleeve"}))
        self.assertEqual(create_user.status_code, 201)
        
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"ryan", "password":"sleeve"}))
        self.assertEqual(login_user.status_code, 200)
        response = json.loads(login_user.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as ryan')
        self.user_access_token = response['access_token']

        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"keem", "password":"sleeve"}))
        self.assertEqual(create_user.status_code, 201)
        
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"keem", "password":"sleeve"}))
        self.assertEqual(login_user.status_code, 200)
        response = json.loads(login_user.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as keem')
        self.wrong_user_access_token = response['access_token']

        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', headers={'Authorization': f"Bearer {self.user_access_token}"}, data=json.dumps(test_parcel))

        put_request = self.app_client.put("/api/v1/parcels/1/destination", data=json.dumps({"destination":"masaka"}), headers={'Authorization': f"Bearer {self.wrong_user_access_token}"})
        response = json.loads(put_request.data.decode())
        self.assertEqual(put_request.status_code, 400)
        self.assertEqual(response['message'], "Invalid request! You do not have rights to change the destination of parcel 1")


if __name__ == ('__main__'):
    unittest.main()