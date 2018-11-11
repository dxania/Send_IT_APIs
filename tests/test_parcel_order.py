import json
import unittest
from app import app
from app.routes.parcel_routes import *

test_user ={
    "user_id": 1,
    "user_name" : "dee",
	"password": "winx"
}

test_parcel = {
    "user_id":1,
    "pickup_location" : "Kampala",
    "destination": "Namugongo",
    "items": [{"item_name": "Shoes", "item_weight": 40, "unit_delivery_price":2000}]
}

wrong_parcel = {
    "user_id":2,
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
    def test_get_all_parcel_delivery_orders(self):
        create_user = self.app_client.post("/api/v1/users", content_type='application/json', data=json.dumps(test_user))    
        post_request = self.app_client.post("/api/v1/parcels",content_type='application/json',data=json.dumps(test_parcel))      
        get_request = self.app_client.get("/api/v1/parcels")
        self.assertEqual(create_user.status_code, 201)
        self.assertEqual(post_request.status_code, 201)
        self.assertEqual(get_request.status_code, 200)

    def test_empty_parcel_delivery_order_list(self):
        get_request = self.app_client.get("/api/v1/parcels")
        response = json.loads(get_request.data.decode())
        self.assertEqual(response['message'], 'There are no parcel delivery orders')
        self.assertEqual(get_request.status_code, 200)

    def test_get_all_parcel_delivery_orders_by_specific_user(self):
        create_user = self.app_client.post("/api/v1/users", content_type='application/json', data=json.dumps(test_user))
        post_request = self.app_client.post("/api/v1/parcels",content_type='application/json',data=json.dumps(test_parcel))
        get_request = self.app_client.get("/api/v1/users/1/parcels")
        # self.assertEqual(create_user.status_code, 201)
        self.assertEqual(post_request.status_code, 201)
        self.assertEqual(get_request.status_code, 200)

    def test_get_all_parcel_delivery_orders_by_non_user(self):
        post_request = self.app_client.post("/api/v1/parcels",
                                 content_type='application/json',
                                 data=json.dumps(test_parcel)
                    )
        get_request = self.app_client.get("/api/v1/users/2/parcels")
        response = json.loads(get_request.data.decode())
        self.assertEqual(response['message'], 'There are no parcels delivery orders created by that user or the user does not exist')
        self.assertEqual(get_request.status_code, 200)

    # def test_cancel_parcel_delivery_order(self):
    #     parcel = {
    #         "user_id":1,
    #         "parcel_id" : 9,
    #         "pickup_location" : "Kampala",
    #         "destination": "Namugongo",
    #         # "no_of_items": 2,
    #         "items": [{"item_name": "Shoes", "item_weight": 40, "unit_delivery_price":2000}]
            # "total_weight":41,
            # "total_price": 65000
        # }
        # put_request = self.app_client.put("/api/v1/users/1/9/cancel",
        #                          content_type='application/json',
        #                          data=json.dumps(parcel)
        #             )
        # self.assertEqual(put_request.status_code, 202)


#     def test_get_parcel(self):
#         parcel = {
#             "user_id":1,
#             "parcel_id" : 9,
#             "pickup_location" : "Kampala",
#             "destination": "Namugongo",
#             # "no_of_items": 2,
#             "items": [{"item_name": "Shoes", "item_weight": 40, "unit_delivery_price":2000}]
#             # "total_weight":41,
#             # "total_price": 65000
#         }
#         post_request = self.app_client.post("/api/v1/parcels",
#                                  content_type='application/json',
#                                  data=json.dumps(parcel)
#                     )
#         self.assertEqual(post_request.status_code, 201)
#         get_request = self.app_client.get("/api/v1/parcels/1")
#         self.assertEqual(get_request.status_code, 200)
    
#     def test_create_parcel(self):
#         parcel = {
#             "user_id":1,
#             "parcel_id" : 9,
#             "pickup_location" : "Kampala",
#             "destination": "Namugongo",
#             # "no_of_items": 2,
#             "items": [{"item_name": "Shoes", "item_weight": 40, "unit_delivery_price":2000}]
#             # "total_weight":41,
#             # "total_price": 65000
#         }
#         response = self.app_client.post("/api/v1/parcels",
#                                  content_type='application/json',
#                                  data=json.dumps(parcel)
#                     )
#         self.assertEqual(response.status_code, 201)

# class MethodsReturnType(Base):
#     """
#     Tests all aspects of non existent output
#     Tests include: retrieving a non existent parcel record
#     """
#     # def test_get_empty_list(self):
#     #     get_request = self.app_client.get("/api/v1/parcels")
#     #     response = json.loads(get_request.data.decode())
#     #     self.assertEqual('There are no parcel delivery orders', response["message"])
#     #     self.assertEqual(get_request.status_code, 204)

#     def test_get_non_existent_parcel_record(self):
#         get_request = self.app_client.get("/api/v1/parcels/9999")
#         # response = json.loads(get_request.data.decode())
#         # self.assertEqual(response['message'], 'There is no parcel delivery order matching that ID')
#         self.assertEqual(get_request.status_code, 204)

# class Set(Base):
#     """
#     Tests all aspects of setting attributes
#     Tests include: setting attributes of wrong type, 
#     setting attributes outside their constraints, setting empty attributes.
#     """
#     def test_pickup_location_required(self):
#         parcel = {
#             "user_id":1,
#             "parcel_id" : 9,
#             "pickup_location" : "",
#             "destination": "Namugongo",
#             "no_of_items": 2,
#             "items": [{"item_name": "Shoes", "item_weight": 40, "unit_delivery_price":2000, "amount":60000},
#                         {"item_name": "Letter", "item_weight": 1, "unit_delivery_price":500, "amount":500}],
#             "total_weight":41,
#             "total_price": 65000
#         }
#         post_request = self.app_client.post("/api/v1/parcels",
#                                         content_type='application/json',
#                                         data=json.dumps(parcel))
#         response = json.loads(post_request.data.decode())
#         self.assertIn("Pickup location is required", response['message'])
#         self.assertEqual(post_request.status_code, 400)

#     def test_destination_required(self):
#         parcel = {
#             "user_id":1,
#             "parcel_id" : 9,
#             "pickup_location" : "Kampala",
#             "destination": "",
#             "no_of_items": 2,
#             "items": [{"item_name": "Shoes", "item_weight": 40, "unit_delivery_price":2000, "amount":60000},
#                         {"item_name": "Letter", "item_weight": 1, "unit_delivery_price":500, "amount":500}],
#             "total_weight":41,
#             "total_price": 65000
#         }
#         post_request = self.app_client.post("/api/v1/parcels",
#                                         content_type='application/json',
#                                         data=json.dumps(parcel))
#         response = json.loads(post_request.data.decode())
#         self.assertIn("Destination is required", response['message'])
#         self.assertEqual(post_request.status_code, 400)

#     def test_pickup_location_letters(self):
#         parcel = {
#             "user_id":1,
#             "parcel_id" : 9,
#             "pickup_location" : "90",
#             "destination": "Namugongo",
#             "no_of_items": 2,
#             "items": [{"item_name": "Shoes", "item_weight": 40, "unit_delivery_price":2000, "amount":60000},
#                         {"item_name": "Letter", "item_weight": 1, "unit_delivery_price":500, "amount":500}],
#             "total_weight":41,
#             "total_price": 65000
#         }
#         post_request = self.app_client.post("/api/v1/parcels",
#                                         content_type='application/json',
#                                         data=json.dumps(parcel))
#         response = json.loads(post_request.data.decode())
#         self.assertIn("Pickup location must be letters", response['message'])
#         self.assertEqual(post_request.status_code, 400)

#     def test_destination_letters(self):
#         parcel = {
#             "user_id":1,
#             "parcel_id" : 9,
#             "pickup_location" : "Kampala",
#             "destination": "89",
#             "no_of_items": 2,
#             "items": [{"item_name": "Shoes", "item_weight": 40, "unit_delivery_price":2000, "amount":60000},
#                         {"item_name": "Letter", "item_weight": 1, "unit_delivery_price":500, "amount":500}],
#             "total_weight":41,
#             "total_price": 65000
#         }
#         post_request = self.app_client.post("/api/v1/parcels",
#                                         content_type='application/json',
#                                         data=json.dumps(parcel))
#         response = json.loads(post_request.data.decode())
#         self.assertIn("Destination must be letters", response['message'])
#         self.assertEqual(post_request.status_code, 400)

#     # def test_number_of_items_required(self):
#     #     parcel = {
#     #             "parcel_id" : 9,
#     #             "pickup_location" : "Kampala",
#     #             "destination": "Namugongo",
#     #             "items": [{"item_name": "Shoes", "item_weight": 40, "unit_delivery_price":2000, "amount":60000},
#     #                         {"item_name": "Letter", "item_weight": 1, "unit_delivery_price":500, "amount":500}],
#     #             "total_weight":41,
#     #             "total_price": 65000
#     #     }
#     #     post_request = self.app_client.post("/api/v1/parcels",
#     #                                     content_type='application/json',
#     #                                     data=json.dumps(parcel))
#     #     response = json.loads(post_request.data.decode())
#     #     self.assertIn("Number of items is required", response['message'])
#     #     self.assertEqual(post_request.status_code, 400)    

#     def test_parcel_items_required(self):
#         parcel = {
#             "user_id":1,
#             "parcel_id" : 9,
#             "pickup_location" : "Kampala",
#             "destination": "Namugongo",
#             "no_of_items": 2,
#             "items": "",
#             "total_weight":41,
#             "total_price": 65000
#         }
#         post_request = self.app_client.post("/api/v1/parcels",
#                                         content_type='application/json',
#                                         data=json.dumps(parcel))
#         response = json.loads(post_request.data.decode())
#         self.assertIn("Enter at least one item", response['message'])
#         self.assertEqual(post_request.status_code, 400)

    # def test_parcel_itemname_required(self):
    #     parcel = {
    #             "parcel_id" : 9,
    #             "pickup_location" : "Kampala",
    #             "destination": "Namugongo",
    #             "no_of_items": 2,
    #             "items": [{"item_name": "", "item_weight": 40, "unit_delivery_price":2000, "amount":60000},
    #                         {"item_name": "Letter", "item_weight": 1, "unit_delivery_price":500, "amount":500}],
    #             "total_weight":41,
    #             "total_price": 65000
    #     }
    #     post_request = self.app_client.post("/api/v1/parcels",
    #                                     content_type='application/json',
    #                                     data=json.dumps(parcel))
    #     response = json.loads(post_request.data.decode())
    #     self.assertIn("Parcel item name is required", response['message'])
    #     self.assertEqual(post_request.status_code, 400)

    # def test_itemname_letters(self):
    #     parcel = {
    #             "parcel_id" : 9,
    #             "pickup_location" : "Kampala",
    #             "destination": "Namugongo",
    #             "no_of_items": 2,
    #             "items": [{"item_name": "22", "item_weight": 40, "unit_delivery_price":2000, "amount":60000},
    #                         {"item_name": "Letter", "item_weight": 1, "unit_delivery_price":500, "amount":500}],
    #             "total_weight":41,
    #             "total_price": 65000
    #     }
    #     post_request = self.app_client.post("/api/v1/parcels",
    #                                     content_type='application/json',
    #                                     data=json.dumps(parcel))
    #     response = json.loads(post_request.data.decode())
    #     self.assertIn("Parcel item name must be letters", response['message'])
    #     self.assertEqual(post_request.status_code, 400)

    # def test_itemweight_required(self):
    #     parcel = {
    #             "parcel_id" : 9,
    #             "pickup_location" : "Kampala",
    #             "destination": "Namugongo",
    #             "no_of_items": 2,
    #             "items": [{"item_name": "Shoes", "item_weight": "", "unit_delivery_price":2000, "amount":60000},
    #                         {"item_name": "Letter", "item_weight": 1, "unit_delivery_price":500, "amount":500}],
    #             "total_weight":41,
    #             "total_price": 65000
    #     }
    #     post_request = self.app_client.post("/api/v1/parcels",
    #                                     content_type='application/json',
    #                                     data=json.dumps(parcel))
    #     response = json.loads(post_request.data.decode())
    #     self.assertIn("Parcel item weight is required", response['message'])
    #     self.assertEqual(post_request.status_code, 400)

    # def test_itemweight_number(self):
    #     parcel = {
    #         "parcel_id" : 9,
    #         "pickup_location" : "Kampala",
    #         "destination": "Namugongo",
    #         "no_of_items": 2,
    #         "items": [{"item_name": "Shoes", "item_weight": "x", "unit_delivery_price":2000, "amount":60000},
    #                     {"item_name": "Letter", "item_weight": 1, "unit_delivery_price":500, "amount":500}],
    #         "total_weight":41,
    #         "total_price": 65000
    #     }
    #     post_request = self.app_client.post("/api/v1/parcels",
    #                                     content_type='application/json',
    #                                     data=json.dumps(parcel))
    #     response = json.loads(post_request.data.decode())
    #     self.assertIn("Parcel item weight must be an integer", response['message'])
    #     self.assertEqual(post_request.status_code, 400)

    # def test_item_unit_delivery_price_required(self):
    #     parcel = {
    #             "parcel_id" : 9,
    #             "pickup_location" : "Kampala",
    #             "destination": "Namugongo",
    #             "no_of_items": 2,
    #             "items": [{"item_name": "Shoes", "item_weight": 40, "unit_delivery_price":"", "amount":60000},
    #                         {"item_name": "Letter", "item_weight": 1, "unit_delivery_price":500, "amount":500}],
    #             "total_weight":41,
    #             "total_price": 65000
    #     }
    #     post_request = self.app_client.post("/api/v1/parcels",
    #                                     content_type='application/json',
    #                                     data=json.dumps(parcel))
    #     response = json.loads(post_request.data.decode())
    #     self.assertIn("Parcel item unit delivery price is required", response['message'])
    #     self.assertEqual(post_request.status_code, 400)

    # def test_item_unit_delivery_price_number(self):
    #     parcel = {
    #         "parcel_id" : 9,
    #         "pickup_location" : "Kampala",
    #         "destination": "Namugongo",
    #         "no_of_items": 2,
    #         "items": [{"item_name": "Shoes", "item_weight": 40, "unit_delivery_price":"x", "amount":60000},
    #                     {"item_name": "Letter", "item_weight": 1, "unit_delivery_price":500, "amount":500}],
    #         "total_weight":41,
    #         "total_price": 65000
    #     }
    #     post_request = self.app_client.post("/api/v1/parcels",
    #                                     content_type='application/json',
    #                                     data=json.dumps(parcel))
    #     response = json.loads(post_request.data.decode())
    #     self.assertIn("Parcel item unit delivery price must be an integer", response['message'])
    #     self.assertEqual(post_request.status_code, 400)

    # def test_item_total_delivery_price_required(self):
    #     parcel = {
    #             "parcel_id" : 9,
    #             "pickup_location" : "Kampala",
    #             "destination": "Namugongo",
    #             "no_of_items": 2,
    #             "items": [{"item_name": "Shoes", "item_weight": 40, "unit_delivery_price":"", "amount":60000},
    #                         {"item_name": "Letter", "item_weight": 1, "unit_delivery_price":500, "amount":500}],
    #             "total_weight":41,
    #             "total_price": 65000
    #     }
    #     post_request = self.app_client.post("/api/v1/parcels",
    #                                     content_type='application/json',
    #                                     data=json.dumps(parcel))
    #     response = json.loads(post_request.data.decode())
    #     self.assertIn("Parcel item total delivery price is required", response['message'])
    #     self.assertEqual(post_request.status_code, 400)

    # def test_item_total_delivery_price_number(self):
    #     parcel = {
    #         "parcel_id" : 9,
    #         "pickup_location" : "Kampala",
    #         "destination": "Namugongo",
    #         "no_of_items": 2,
    #         "items": [{"item_name": "Shoes", "item_weight": 40, "unit_delivery_price":"x", "amount":"p"},
    #                     {"item_name": "Letter", "item_weight": 1, "unit_delivery_price":500, "amount":500}],
    #         "total_weight":41,
    #         "total_price": 65000
    #     }
    #     post_request = self.app_client.post("/api/v1/parcels",
    #                                     content_type='application/json',
    #                                     data=json.dumps(parcel))
    #     response = json.loads(post_request.data.decode())
    #     self.assertIn("Parcel item total delivery price must be an integer", response['message'])
    #     self.assertEqual(post_request.status_code, 400)


if __name__ == ('__main__'):
    unittest.main()