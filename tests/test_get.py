import json
import unittest
from app import app
from app.routes.parcel_routes import *
from app.routes.user_routes import *
from app.controllers.db import DatabaseConnection
from tests.test_create import Base

test_user ={
    "user_name" : "alex",
    "password": "together"
}

test_parcel = {
    "recipient_name" : "cara",
    "recipient_mobile": 1234567890,
    "pickup_location" : "op",
    "destination": "ki",
    "weight":200
    }


class Endpoints(Base):
    """
    Tests all aspects of endpoints
    Tests include: getting all parcel delivery orders, getting a particular parcel delivery order,
    getting all parcel delivery orders by a specific user.  
    """
    def test_get_empty_parcel_delivery_order_list(self):
        self.admin_login()
        get_request = self.app_client.get("/api/v1/parcels", 
            headers={'Authorization': f"Bearer {self.admin_access_token}"})
        get_response = json.loads(get_request.data.decode())
        self.assertEqual(get_response['message'], "There are no parcel delivery orders")
        self.assertEqual(get_request.status_code, 200)

    def test_get_all_parcel_delivery_orders(self):
        self.admin_login()
        self.user_login()
        post_request = self.app_client.post("/api/v1/parcels",content_type='application/json',data=json.dumps(test_parcel), 
            headers={'Authorization': f"Bearer {self.user_access_token}"})      
        get_request = self.app_client.get("/api/v1/parcels", headers={'Authorization': f"Bearer {self.admin_access_token}"})
        self.assertEqual(post_request.status_code, 201)
        self.assertEqual(get_request.status_code, 200)


    def test_get_all_parcel_delivery_orders_by_specific_user(self):
        self.admin_login()
        self.user_login()
        post_request = self.app_client.post("/api/v1/parcels",content_type='application/json',data=json.dumps(test_parcel), 
            headers={'Authorization': f"Bearer {self.user_access_token}"})
        get_request = self.app_client.get("/api/v1/users/mike/parcels", headers={'Authorization': f"Bearer {self.admin_access_token}"})
        self.assertEqual(get_request.status_code, 200)

    def test_get_parcel(self):
        self.admin_login()
        self.user_login()
        post_request = self.app_client.post("/api/v1/parcels",content_type='application/json',data=json.dumps(test_parcel), 
            headers={'Authorization': f"Bearer {self.user_access_token}"})
        get_request = self.app_client.get("/api/v1/parcels/1", headers={'Authorization': f"Bearer {self.admin_access_token}"})
        self.assertEqual(get_request.status_code, 200)

    def test_get_all_parcel_delivery_orders_by_invalid_user(self):
        self.admin_login()
        self.user_login()
        post_request = self.app_client.post("/api/v1/parcels",content_type='application/json',data=json.dumps(test_parcel), 
            headers={'Authorization': f"Bearer {self.user_access_token}"})
        get_request = self.app_client.get("/api/v1/users/1/parcels", 
            headers={'Authorization': f"Bearer {self.admin_access_token}"})
        response3 = json.loads(get_request.data.decode())
        self.assertEqual(response3['message'], 'Enter a valid user name')
        self.assertEqual(get_request.status_code, 400)

    def test_get_empty_parcel_delivery_order_list_by_user(self):
        self.admin_login()
        get_request = self.app_client.get("/api/v1/users/sam/parcels", 
            headers={'Authorization': f"Bearer {self.admin_access_token}"})
        response3 = json.loads(get_request.data.decode())
        self.assertEqual(response3['message'], 'There are no parcels delivery orders created by sam')
        self.assertEqual(get_request.status_code, 200)


    def test_unauthorized_user_get_parcel(self):
        self.user_login()
        self.user2_login() 
        post_request = self.app_client.post("/api/v1/parcels",content_type='application/json', data=json.dumps(test_parcel), 
            headers={'Authorization': f"Bearer {self.user_access_token}"})
        get_request = self.app_client.get("/api/v1/parcels/1", headers={'Authorization': f"Bearer {self.user_access_token2}"})
        response = json.loads(get_request.data.decode())
        self.assertEqual(response['message'], "You do not have access to parcel delivery order 1")
        self.assertEqual(get_request.status_code, 401)

    def test_get_non_existent_parcel(self):
        self.admin_login()

        get_request = self.app_client.get("/api/v1/parcels/900", 
            headers={'Authorization': f"Bearer {self.admin_access_token}"})
        response = json.loads(get_request.data.decode())
        self.assertEqual(response['message'], "There is no parcel with ID 900")
        self.assertEqual(get_request.status_code, 404)

if __name__ == ('__main__'):
    unittest.main()