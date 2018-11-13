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

    def test_cancel_parcel_delivery_order(self):
        create_user = self.app_client.post("/api/v1/users", content_type='application/json', data=json.dumps(test_user))
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', data=json.dumps(test_parcel))
        put_request = self.app_client.put("/api/v1/parcels/1/cancel")
        self.assertEqual(create_user.status_code, 201)
        self.assertEqual(post_request.status_code, 201)
        self.assertEqual(put_request.status_code, 200)

    def test_cancel_parcel_delivery_order_user(self):
        create_user = self.app_client.post("/api/v1/users", content_type='application/json', data=json.dumps(test_user))
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', data=json.dumps(test_parcel))
        put_request = self.app_client.put("/api/v1/users/1/1/cancel")
        self.assertEqual(put_request.status_code, 200)

    def test_cancel_non_existent_parcel_delivery_order(self):
        put_request = self.app_client.put("/api/v1/parcels/100/cancel")
        response = json.loads(put_request.data.decode())
        self.assertEqual(put_request.status_code, 200)
        self.assertEqual(response['message'], "There is no parcel with that ID")

    def test_cancel_non_existent_parcel_delivery_order_user(self):
        put_request = self.app_client.put("/api/v1/users/1/100/cancel")
        response = json.loads(put_request.data.decode())
        self.assertEqual(put_request.status_code, 200)
        self.assertEqual(response['message'], "There is no parcel with that ID")

    def test_wrong_user_cancel_parcel_delivery_order(self):
        put_request = self.app_client.put("/api/v1/users/200/1/cancel")
        response = json.loads(put_request.data.decode())
        self.assertEqual(put_request.status_code, 200)
        self.assertEqual(response['message'], "You dont have rights to cancel this parcel delivery order")


if __name__ == ('__main__'):
    unittest.main()