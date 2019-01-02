import json
import unittest
from app import app
from app.routes.parcel_routes import *
from app.routes.user_routes import *
from app.controllers.db import DatabaseConnection
from tests.test_create import Base

test_parcel = {
    "description" : "Electronics",
    "recipient_name" : "cara",
    "recipient_mobile": "0777777999",
    "pickup_location" : "Nakawa, Uganda",
    "destination": "Kampala, Uganda",
    "weight":200
    }

class Endpoints(Base):
    """
    Tests all aspects of get parcel endpoints
    Tests include: getting all parcel delivery orders, getting parcel delivery orders by a specific user, getting one
    parcel delivery order.  
    """
    def test_get_empty_parcel_delivery_order_list(self):
        self.admin_login()
        get_request = self.app_client.get("/api/v1/parcels", 
            headers={'Authorization': f"Bearer {self.admin_access_token}"})
        get_response = json.loads(get_request.data)
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
        get_request = self.app_client.get("/api/v1/users/1/parcels", headers={'Authorization': f"Bearer {self.admin_access_token}"})
        self.assertEqual(get_request.status_code, 200)

    def test_get_parcel(self):
        self.admin_login()
        self.user_login()
        post_request = self.app_client.post("/api/v1/parcels",content_type='application/json',data=json.dumps(test_parcel), 
            headers={'Authorization': f"Bearer {self.user_access_token}"})
        get_request = self.app_client.get("/api/v1/parcels/1", headers={'Authorization': f"Bearer {self.admin_access_token}"})
        self.assertEqual(get_request.status_code, 200)

    def test_get_empty_parcel_delivery_order_list_by_user(self):
        self.admin_login()
        self.user_login()
        get_request = self.app_client.get("/api/v1/users/1/parcels", headers={'Authorization': f"Bearer {self.admin_access_token}"})
        response = json.loads(get_request.data)
        self.assertEqual(response['message'], 'There are no parcels delivery orders created by user 1')
        self.assertEqual(get_request.status_code, 200)

    def test_invalid_access_to_users_parcels(self):
        self.user_login()
        post_request = self.app_client.post("/api/v1/parcels",content_type='application/json', data=json.dumps(test_parcel), 
            headers={'Authorization': f"Bearer {self.user_access_token}"})
        self.user2_login()
        get_request = self.app_client.get("/api/v1/users/1/parcels", headers={'Authorization': f"Bearer {self.user_access_token2}"})
        response = json.loads(get_request.data)
        self.assertEqual(response['message'], "You can only view parcels you created")
        self.assertEqual(get_request.status_code, 401)

    def test_invalid_access_to_all_parcels(self):
        self.user_login()
        post_request = self.app_client.post("/api/v1/parcels",content_type='application/json', data=json.dumps(test_parcel), 
            headers={'Authorization': f"Bearer {self.user_access_token}"})
        get_request = self.app_client.get("/api/v1/parcels", headers={'Authorization': f"Bearer {self.user_access_token}"})
        response = json.loads(get_request.data)
        self.assertEqual(response['message'], "You can only view parcels you created")
        self.assertEqual(get_request.status_code, 401)
        
    def test_unauthorized_user_get_parcel(self):
        self.user_login()
        self.user2_login() 
        post_request = self.app_client.post("/api/v1/parcels",content_type='application/json', data=json.dumps(test_parcel), 
            headers={'Authorization': f"Bearer {self.user_access_token}"})
        get_request = self.app_client.get("/api/v1/parcels/1", headers={'Authorization': f"Bearer {self.user_access_token2}"})
        response = json.loads(get_request.data)
        self.assertEqual(response['message'], "You can only view parcels you created")
        self.assertEqual(get_request.status_code, 401)

    def test_get_non_existent_parcel(self):
        self.admin_login()
        get_request = self.app_client.get("/api/v1/parcels/900", 
            headers={'Authorization': f"Bearer {self.admin_access_token}"})
        response = json.loads(get_request.data)
        self.assertEqual(response['message'], "There is no parcel with ID 900")
        self.assertEqual(get_request.status_code, 404)

if __name__ == ('__main__'):
    unittest.main()