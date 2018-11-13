import json
import unittest
from app import app
from app.routes.parcel_routes import *
from app.routes.user_routes import *

test_user ={
    "user_name" : "alex",
    "password": "1was"
}

test_parcel = {
    "user_id":1,
    "recipient_name": "Corn",
    "recipient_mobile": 1234567890,
    "pickup_location" : "Kampala",
    "destination": "Namugongo",
    "items": [{"item_name": "Shoes", "item_weight": 40}]
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
    Tests include: getting all parcel delivery orders, getting a particular parcel delivery order,
    getting all parcel delivery orders by a specific user.  
    """
    def test_get_empty_parcel_delivery_order_list(self):
        get_request = self.app_client.get("/api/v1/parcels")
        response = json.loads(get_request.data.decode())
        # self.assertEqual(response['message'], 'There are no parcel delivery orders')
        self.assertEqual(get_request.status_code, 200)

    def test_get_all_parcel_delivery_orders(self):
        create_user = self.app_client.post("/api/v1/users", content_type='application/json', data=json.dumps(test_user))    
        post_request = self.app_client.post("/api/v1/parcels",content_type='application/json',data=json.dumps(test_parcel))      
        get_request = self.app_client.get("/api/v1/parcels")
        # self.assertEqual(create_user.status_code, 201)
        self.assertEqual(post_request.status_code, 201)
        self.assertEqual(get_request.status_code, 200)


    def test_get_all_parcel_delivery_orders_by_specific_user(self):
        get_request = self.app_client.get("/api/v1/users/1/parcels")
        self.assertEqual(get_request.status_code, 200)

    def test_get_all_parcel_delivery_orders_by_non_user(self):
        get_request = self.app_client.get("/api/v1/users/2/parcels")
        response = json.loads(get_request.data.decode())
        self.assertEqual(response["message"], "There are no parcels delivery orders created by that user or the user does not exist")
        self.assertEqual(get_request.status_code, 200)

    def test_get_parcel(self):
        get_request = self.app_client.get("/api/v1/parcels/1")
        self.assertEqual(get_request.status_code, 200)

    def test_get_non_existent_parcel(self):
        get_request = self.app_client.get("/api/v1/parcels/400")
        response = json.loads(get_request.data.decode())
        self.assertEqual(response['message'], "Parcel with ID 400 does not exist")
        self.assertEqual(get_request.status_code, 200)

if __name__ == ('__main__'):
    unittest.main()