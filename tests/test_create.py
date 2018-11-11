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
    "pickup_location" : "Kampala",
    "destination": "Namugongo",
    "items": [{"item_name": "Shoes", "item_weight": 40, "unit_delivery_price":2000}]
}

class Base(unittest.TestCase):
    """Base class for tests. 
    This class defines a common `setUp` 
    method that defines attributes which 
    are used in the various tests.
    """

    def setUp(self):
        self.app_client = app.test_client()


class Endpoints(Base):
    """
    Tests all aspects of endpoints
    Tests include: creating a parcel delivery order, getting all parcel delivery orders,
    getting a particular parcel delivery order, canceling a parcel delivery order,
    getting all parcel delivery orders by a specific user.  
    """
    def test_non_user_create_parcel(self):
        parcel = {
            "user_id":100,
            "pickup_location" : "Kampala",
            "destination": "Namugongo",
            "items": [{"item_name": "Shoes", "item_weight": 40, "unit_delivery_price":2000}]
        }
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', data=json.dumps(parcel))
        self.assertEqual(response.status_code, 200)
        response = json.loads(post_request.data.decode())
        self.assertEqual(reponse["message"], "You dont have rights to create a parcel delivery order")


    def test_create_parcel(self):
        create_user = self.app_client.post("/api/v1/users", content_type='application/json', data=json.dumps(test_user))
        response = self.app_client.post("/api/v1/parcels", content_type='application/json', data=json.dumps(test_parcel))
        # self.assertEqual(create_user.status_code, 201)
        self.assertEqual(response.status_code, 201)

    def test_non_user_create_parcel(self):
        # create_user = self.app_client.post("/api/v1/users", content_type='application/json', data=json.dumps(user))
        response = self.app_client.post("/api/v1/parcels", content_type='application/json', data=json.dumps(test_parcel))
        # self.assertEqual(create_user.status_code, 201)
        self.assertEqual(response.status_code, 201)


class Set(Base):
    """
    Tests all aspects of setting attributes
    Tests include: setting attributes of wrong type, setting attributes outside their constraints, setting empty attributes.
    """
    def test_userid_int(self):
        create_user = self.app_client.post("/api/v1/users", content_type='application/json', data=json.dumps(test_user))
        parcel = {
            "user_id": "p",
            "pickup_location" : "Najja",
            "destination": "Namugongo",
            "items": [{"item_name": "Shoes", "item_weight": 40, "unit_delivery_price":2000}]
        }
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', data=json.dumps(parcel))
        response = json.loads(post_request.data.decode())
        self.assertIn("Enter a valid user ID", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_userid_required(self):
        create_user = self.app_client.post("/api/v1/users", content_type='application/json', data=json.dumps(test_user))
        parcel = {
            "pickup_location" : "Najja",
            "destination": "Namugongo",
            "items": [{"item_name": "Shoes", "item_weight": 40, "unit_delivery_price":2000}]
        }
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', data=json.dumps(parcel))
        response = json.loads(post_request.data.decode())
        self.assertIn("User ID is required", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_pickup_location_required(self):
        create_user = self.app_client.post("/api/v1/users", content_type='application/json', data=json.dumps(test_user))
        parcel = {
            "user_id":1,
            "pickup_location" : "",
            "destination": "Namugongo",
            "items": [{"item_name": "Shoes", "item_weight": 40, "unit_delivery_price":2000}]
        }
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', data=json.dumps(parcel))
        response = json.loads(post_request.data.decode())
        self.assertIn("Pickup location is required", response['message'])
        self.assertEqual(post_request.status_code, 400)


    def test_destination_required(self):
        create_user = self.app_client.post("/api/v1/users", content_type='application/json', data=json.dumps(test_user))
        parcel = {
            "user_id":1,
            "pickup_location" : "Kampala",
            "destination": "",
            "items": [{"item_name": "Shoes", "item_weight": 40, "unit_delivery_price":2000}]
        }
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', data=json.dumps(parcel))
        response = json.loads(post_request.data.decode())
        self.assertIn("Destination is required", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_pickup_location_letters(self):
        create_user = self.app_client.post("/api/v1/users", content_type='application/json', data=json.dumps(test_user))
        parcel = {
            "user_id":1,
            "pickup_location" : "90",
            "destination": "Namugongo",
            "items": [{"item_name": "Shoes", "item_weight": 40, "unit_delivery_price":2000}]
        }
        post_request = self.app_client.post("/api/v1/parcels",
                                        content_type='application/json',
                                        data=json.dumps(parcel))
        response = json.loads(post_request.data.decode())
        self.assertIn("Pickup location must be letters", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_destination_letters(self):
        create_user = self.app_client.post("/api/v1/users", content_type='application/json', data=json.dumps(test_user))
        parcel = {
            "user_id":1,
            "pickup_location" : "Kampala",
            "destination": "89",
            "items": [{"item_name": "Shoes", "item_weight": 40, "unit_delivery_price":2000}]
        }
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', data=json.dumps(parcel))
        response = json.loads(post_request.data.decode())
        self.assertIn("Destination must be letters", response['message'])
        self.assertEqual(post_request.status_code, 400)
   

    def test_parcel_items_required(self):
        create_user = self.app_client.post("/api/v1/users", content_type='application/json', data=json.dumps(test_user))
        parcel = {
            "user_id":1,
            "pickup_location" : "Kampala",
            "destination": "Namugongo",
            "items": ""
        }
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', data=json.dumps(parcel))
        response = json.loads(post_request.data.decode())
        self.assertIn("Enter at least one item", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_parcel_items_list(self):
        create_user = self.app_client.post("/api/v1/users", content_type='application/json', data=json.dumps(test_user))
        parcel = {
            "user_id":1,
            "pickup_location" : "Kampala",
            "destination": "Namugongo",
            "items": "cook"
        }
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', data=json.dumps(parcel))
        response = json.loads(post_request.data.decode())
        self.assertIn("Items must be a list of dictionaries", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_parcel_itemname_required(self):
        create_user = self.app_client.post("/api/v1/users", content_type='application/json', data=json.dumps(test_user))
        parcel = {
                "user_id":1,
                "pickup_location" : "Kampala",
                "destination": "Namugongo",
                "items": [{"item_name": "", "item_weight": 40, "unit_delivery_price":2000}]
        }
        post_request = self.app_client.post("/api/v1/parcels",
                                        content_type='application/json',
                                        data=json.dumps(parcel))
        response = json.loads(post_request.data.decode())
        self.assertIn("Parcel item name is required", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_itemname_letters(self):
        create_user = self.app_client.post("/api/v1/users", content_type='application/json', data=json.dumps(test_user))
        parcel = {
                "user_id" : 1,
                "pickup_location" : "Kampala",
                "destination": "Namugongo",
                "items": [{"item_name": "22", "item_weight": 40, "unit_delivery_price":2000}]
        }
        post_request = self.app_client.post("/api/v1/parcels",content_type='application/json',data=json.dumps(parcel))
        response = json.loads(post_request.data.decode())
        self.assertIn("Parcel item name must be letters", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_itemweight_required(self):
        create_user = self.app_client.post("/api/v1/users", content_type='application/json', data=json.dumps(test_user))
        parcel = {
                "user_id" : 9,
                "pickup_location" : "Kampala",
                "destination": "Namugongo",
                "items": [{"item_name": "Shoes", "item_weight": "", "unit_delivery_price":2000}]
        }
        post_request = self.app_client.post("/api/v1/parcels",
                                        content_type='application/json',
                                        data=json.dumps(parcel))
        response = json.loads(post_request.data.decode())
        self.assertIn("Parcel item weight is required", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_itemweight_number(self):
        create_user = self.app_client.post("/api/v1/users", content_type='application/json', data=json.dumps(test_user))
        parcel = {
            "user_id" : 9,
            "pickup_location" : "Kampala",
            "destination": "Namugongo",
            "items": [{"item_name": "Shoes", "item_weight": "x", "unit_delivery_price":2000}]
        }
        post_request = self.app_client.post("/api/v1/parcels",
                                        content_type='application/json',
                                        data=json.dumps(parcel))
        response = json.loads(post_request.data.decode())
        self.assertIn("Parcel item weight must be an integer", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_item_unit_delivery_price_required(self):
        parcel = {
                "user_id" : 9,
                "pickup_location" : "Kampala",
                "destination": "Namugongo",
                "items": [{"item_name": "Shoes", "item_weight": 40, "unit_delivery_price":""}]
        }
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', data=json.dumps(parcel))
        response = json.loads(post_request.data.decode())
        self.assertIn("Parcel item unit delivery price is required", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_item_unit_delivery_price_number(self):
        create_user = self.app_client.post("/api/v1/users", content_type='application/json', data=json.dumps(test_user))
        parcel = {
            "user_id" : 1,
            "pickup_location" : "Kampala",
            "destination": "Namugongo",
            "items": [{"item_name": "Shoes", "item_weight": 40, "unit_delivery_price":"x"}]
        }
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', data=json.dumps(parcel))
        response = json.loads(post_request.data.decode())
        self.assertIn("Parcel item unit delivery price must be an integer", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_item_total_delivery_price_required(self):
        create_user = self.app_client.post("/api/v1/users", content_type='application/json', data=json.dumps(test_user))
        parcel = {
                "user_id" : 1,
                "pickup_location" : "Kampala",
                "destination": "Namugongo",
                "items": [{"item_name": "Shoes", "item_weight": 40, "unit_delivery_price":""}]
        }
        post_request = self.app_client.post("/api/v1/parcels",
                                        content_type='application/json',
                                        data=json.dumps(parcel))
        response = json.loads(post_request.data.decode())
        self.assertIn("Parcel item unit delivery price is required", response['message'])
        self.assertEqual(post_request.status_code, 400)

    def test_item_total_delivery_price_number(self):
        create_user = self.app_client.post("/api/v1/users", content_type='application/json', data=json.dumps(test_user))
        parcel = {
            "user_id" : 9,
            "pickup_location" : "Kampala",
            "destination": "Namugongo",
            "items": [{"item_name": "Shoes", "item_weight": 40, "unit_delivery_price":"x"}]
        }
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', data=json.dumps(parcel))
        response = json.loads(post_request.data.decode())
        self.assertIn("Parcel item unit delivery price must be an integer", response['message'])
        self.assertEqual(post_request.status_code, 400)


if __name__ == ('__main__'):
    unittest.main()