import json
import unittest
from app import app
from app.routes.parcel_routes import *
from app.routes.user_routes import *
from app.controllers.db import DatabaseConnection

test_user ={
    "user_name" : "alex",
    "password": "together"
}

test_parcel = {
    "recipient_name" : "cara",
    "recipient_mobile": 1234567890,
    "pickup_location" : "op",
    "destination": "ki",
    "weight":200,
    "total_price":2000
}

db = DatabaseConnection()

class Base(unittest.TestCase):
    """Base class for tests. 
    This class defines a common `setUp` method that defines attributes which are used in the various tests.
    """


    def setUp(self):
        self.app_client = app.test_client()
        db.setUp()

    def tearDown(self):
        db.delete_tables()


class Endpoints(Base):
    """
    Tests all aspects of endpoints
    Tests include: getting all parcel delivery orders, getting a particular parcel delivery order,
    getting all parcel delivery orders by a specific user.  
    """
    def test_get_empty_parcel_delivery_order_list(self):
        admin_login = self.app_client.post("api/v1/auth/login", content_type="application/json", data=json.dumps({"user_name":"admin", "password":"root"}))
        self.assertEqual(admin_login.status_code, 200)
        response = json.loads(admin_login.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as admin')
        self.admin_access_token = response['access_token']

        get_request = self.app_client.get("/api/v1/parcels", headers={'Authorization': f"Bearer {self.admin_access_token}"})
        get_response = json.loads(get_request.data.decode())
        self.assertEqual(get_response['message'], "There are no parcel delivery orders")
        self.assertEqual(get_request.status_code, 200)

    def test_get_all_parcel_delivery_orders(self):
        admin_login = self.app_client.post("api/v1/auth/login", content_type="application/json", data=json.dumps({"user_name":"admin", "password":"root"}))
        self.assertEqual(admin_login.status_code, 200)
        response = json.loads(admin_login.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as admin')
        self.admin_access_token = response['access_token']

        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"nate", "password":"alg"}))
        self.assertEqual(create_user.status_code, 201)
        
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"nate", "password":"alg"}))
        self.assertEqual(login_user.status_code, 200)
        response = json.loads(login_user.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as nate')
        self.user_access_token = response['access_token']

        post_request = self.app_client.post("/api/v1/parcels",content_type='application/json',data=json.dumps(test_parcel), headers={'Authorization': f"Bearer {self.user_access_token}"})      
        get_request = self.app_client.get("/api/v1/parcels", headers={'Authorization': f"Bearer {self.admin_access_token}"})
        self.assertEqual(post_request.status_code, 201)
        self.assertEqual(get_request.status_code, 200)


    def test_get_all_parcel_delivery_orders_by_specific_user(self):
        admin_login = self.app_client.post("api/v1/auth/login", content_type="application/json", data=json.dumps({"user_name":"admin", "password":"root"}))
        self.assertEqual(admin_login.status_code, 200)
        response = json.loads(admin_login.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as admin')
        self.admin_access_token = response['access_token']

        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"mike", "password":"alg"}))
        self.assertEqual(create_user.status_code, 201)
        
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"mike", "password":"alg"}))
        self.assertEqual(login_user.status_code, 200)
        response = json.loads(login_user.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as mike')
        self.user_access_token = response['access_token']

        post_request = self.app_client.post("/api/v1/parcels",content_type='application/json',data=json.dumps(test_parcel), headers={'Authorization': f"Bearer {self.user_access_token}"})

        get_request = self.app_client.get("/api/v1/users/mike/parcels", headers={'Authorization': f"Bearer {self.admin_access_token}"})
        self.assertEqual(get_request.status_code, 200)

    def test_get_all_parcel_delivery_orders_by_invalid_user(self):
        admin_login = self.app_client.post("api/v1/auth/login", content_type="application/json", data=json.dumps({"user_name":"admin", "password":"root"}))
        self.assertEqual(admin_login.status_code, 200)
        response = json.loads(admin_login.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as admin')
        self.admin_access_token = response['access_token']

        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"clem", "password":"alg"}))
        self.assertEqual(create_user.status_code, 201)
        
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"clem", "password":"alg"}))
        self.assertEqual(login_user.status_code, 200)
        response2 = json.loads(login_user.data.decode())
        self.assertEqual(response2['message'], 'You have successfully been logged in as clem')
        self.user_access_token = response2['access_token']

        post_request = self.app_client.post("/api/v1/parcels",content_type='application/json',data=json.dumps(test_parcel), headers={'Authorization': f"Bearer {self.user_access_token}"})

        get_request = self.app_client.get("/api/v1/users/1/parcels", headers={'Authorization': f"Bearer {self.admin_access_token}"})
        response3 = json.loads(get_request.data.decode())
        self.assertEqual(response3['message'], 'Enter a valid user name')
        self.assertEqual(get_request.status_code, 400)

    def test_get_empty_parcel_delivery_order_list_by_user(self):
        admin_login = self.app_client.post("api/v1/auth/login", content_type="application/json", data=json.dumps({"user_name":"admin", "password":"root"}))
        self.assertEqual(admin_login.status_code, 200)
        response = json.loads(admin_login.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as admin')
        self.admin_access_token = response['access_token']

        get_request = self.app_client.get("/api/v1/users/sam/parcels", headers={'Authorization': f"Bearer {self.admin_access_token}"})
        response3 = json.loads(get_request.data.decode())
        self.assertEqual(response3['message'], 'There are no parcels delivery orders created by sam')
        self.assertEqual(get_request.status_code, 200)


    def test_get_parcel(self):
        admin_login = self.app_client.post("api/v1/auth/login", content_type="application/json", data=json.dumps({"user_name":"admin", "password":"root"}))
        self.assertEqual(admin_login.status_code, 200)
        response = json.loads(admin_login.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as admin')
        self.admin_access_token = response['access_token']

        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"clem", "password":"alg"}))
        self.assertEqual(create_user.status_code, 201)
        
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"clem", "password":"alg"}))
        self.assertEqual(login_user.status_code, 200)
        response2 = json.loads(login_user.data.decode())
        self.assertEqual(response2['message'], 'You have successfully been logged in as clem')
        self.user_access_token = response2['access_token']

        post_request = self.app_client.post("/api/v1/parcels",content_type='application/json',data=json.dumps(test_parcel), headers={'Authorization': f"Bearer {self.user_access_token}"})

        get_request = self.app_client.get("/api/v1/parcels/1", headers={'Authorization': f"Bearer {self.admin_access_token}"})
        self.assertEqual(get_request.status_code, 200)

    def test_unauthorized_user_get_parcel(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"susan", "password":"alg"}))
        self.assertEqual(create_user.status_code, 201)
        
        login_user = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"susan", "password":"alg"}))
        self.assertEqual(login_user.status_code, 200)
        response = json.loads(login_user.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as susan')
        self.user_access_token = response['access_token']

        create_user2 = self.app_client.post("/api/v1/auth/signup", content_type='application/json', data=json.dumps({"user_name":"clem", "password":"alg"}))
        self.assertEqual(create_user2.status_code, 201)

        login_user2 = self.app_client.post('/api/v1/auth/login', content_type='application/json', data=json.dumps({"user_name":"clem", "password":"alg"}))
        self.assertEqual(login_user2.status_code, 200)
        response2 = json.loads(login_user2.data.decode())
        self.assertEqual(response2['message'], 'You have successfully been logged in as clem')
        self.user_access_token2 = response2['access_token']
        
        post_request = self.app_client.post("/api/v1/parcels",content_type='application/json',data=json.dumps(test_parcel), headers={'Authorization': f"Bearer {self.user_access_token}"})

        get_request = self.app_client.get("/api/v1/parcels/1", headers={'Authorization': f"Bearer {self.user_access_token2}"})
        response = json.loads(get_request.data.decode())
        self.assertEqual(response['message'], "You do not have access to parcel delivery order 1")
        self.assertEqual(get_request.status_code, 400)

    def test_get_non_existent_parcel(self):
        admin_login = self.app_client.post("api/v1/auth/login", content_type="application/json", data=json.dumps({"user_name":"admin", "password":"root"}))
        self.assertEqual(admin_login.status_code, 200)
        response = json.loads(admin_login.data.decode())
        self.assertEqual(response['message'], 'You have successfully been logged in as admin')
        self.admin_access_token = response['access_token']

        get_request = self.app_client.get("/api/v1/parcels/900", headers={'Authorization': f"Bearer {self.admin_access_token}"})
        response = json.loads(get_request.data.decode())
        self.assertEqual(response['message'], "Parcel with ID 900 does not exist")
        self.assertEqual(get_request.status_code, 200)

if __name__ == ('__main__'):
    unittest.main()