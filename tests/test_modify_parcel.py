import json
import unittest
from app import app
from app.routes.parcel_routes import *
from app.routes.user_routes import *
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
    Tests all aspects of modifying endpoints
    Tests include: changing the present location of a parcel delivery order, changing the destination of a parcel delivery order
    and changing the status of a parcel delivery order.  
    """

    def test_change_present_location(self):
        self.user_login()
        self.admin_login()
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
            headers={'Authorization': f"Bearer {self.user_access_token}"}, data=json.dumps(test_parcel))
        put_request = self.app_client.put("/api/v1/parcels/1/present_location", content_type='application/json', 
            data=json.dumps({"present_location":"Ntinda, Uganda"}), headers={'Authorization': f"Bearer {self.admin_access_token}"})
        response = json.loads(put_request.data.decode())
        self.assertEqual(post_request.status_code, 201)
        self.assertEqual(put_request.status_code, 200)
        self.assertEqual("Present location of parcel 1 changed to Ntinda, Uganda", response['message'])
    
    def test_change_destination(self):
        self.user_login()
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
            headers={'Authorization': f"Bearer {self.user_access_token}"}, data=json.dumps(test_parcel))
        put_request = self.app_client.put("/api/v1/parcels/1/destination", content_type='application/json', 
            data=json.dumps({"destination":"Ntinda, Uganda", "total_price":1000000}), headers={'Authorization': f"Bearer {self.user_access_token}"})
        self.assertEqual(post_request.status_code, 201)
        self.assertEqual(put_request.status_code, 200)
        response = json.loads(put_request.data.decode())
        self.assertEqual("Destination of parcel 1 changed to Ntinda, Uganda", response['message'])
    
    def test_change_status(self):
        # self.user_login()
        self.admin_login()
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
            headers={'Authorization': f"Bearer {self.admin_access_token}"}, data=json.dumps(test_parcel))
        put_request = self.app_client.put("/api/v1/parcels/1/status", content_type='application/json', 
            data=json.dumps({"status":"cancelled"}), headers={'Authorization': f"Bearer {self.admin_access_token}"})
        self.assertEqual(post_request.status_code, 201)
        self.assertEqual(put_request.status_code, 200)
        response = json.loads(put_request.data.decode())
        self.assertEqual("Parcel 1 has been cancelled", response['message'])

    
class Set(Base):
    """
    Tests all aspects of setting wrong attributes
    """
    def test_change_present_location_cancelled_parcel(self):
        self.user_login()
        self.admin_login()
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
            headers={'Authorization': f"Bearer {self.user_access_token}"}, data=json.dumps(test_parcel))
        # cancel_request = self.app_client.put("/api/v1/parcels/1/status", content_type='application/json', 
        #     data=json.dumps({"status":"cancelled"}), headers={'Authorization': f"Bearer {self.admin_access_token}"}) 
        cancel_request = self.app_client.put("/api/v1/parcels/1/status", content_type='application/json', 
            headers={'Authorization': f"Bearer {self.user_access_token}"})
        put_request = self.app_client.put("/api/v1/parcels/1/present_location", content_type='application/json', 
            data=json.dumps({"present_location":"Ntinda, Uganda"}), headers={'Authorization': f"Bearer {self.admin_access_token}"})
        response = json.loads(put_request.data)
        self.assertEqual(post_request.status_code, 201)
        self.assertEqual(cancel_request.status_code, 200)
        self.assertEqual(put_request.status_code, 400)
        self.assertEqual("Present location of parcel 1 can not be changed because it was cancelled or delivered", response['message'])

    def test_change_destination_cancelled_parcel(self):
        self.user_login()
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
            headers={'Authorization': f"Bearer {self.user_access_token}"}, data=json.dumps(test_parcel))
        cancel_request = self.app_client.put("/api/v1/parcels/1/status", content_type='application/json', 
            headers={'Authorization': f"Bearer {self.user_access_token}"}) 
        put_request = self.app_client.put("/api/v1/parcels/1/destination", content_type='application/json', 
            data=json.dumps({"destination":"Ntinda, Uganda", "total_price":1000000}), headers={'Authorization': f"Bearer {self.user_access_token}"})
        response = json.loads(put_request.data)
        self.assertEqual(post_request.status_code, 201)
        self.assertEqual(cancel_request.status_code, 200)
        self.assertEqual(put_request.status_code, 400)
        self.assertEqual("Destination of parcel 1 can not be changed because it was cancelled or delivered", response['message'])

    def test_change_present_location_non_existent_parcel_delivery_order(self):       
        self.admin_login()
        put_request = self.app_client.put("/api/v1/parcels/100/present_location", data=json.dumps({"present_location":"masaka"}), 
            headers={'Authorization': f"Bearer {self.admin_access_token}"})
        response = json.loads(put_request.data)
        self.assertEqual(put_request.status_code, 404)
        self.assertEqual(response['message'], "There is no parcel with ID 100")

    def test_change_destination_non_existent_parcel_delivery_order(self):       
        self.user_login()
        put_request = self.app_client.put("/api/v1/parcels/100/destination", data=json.dumps({"destination":"masaka"}), 
            headers={'Authorization': f"Bearer {self.user_access_token}"})
        response = json.loads(put_request.data.decode())
        self.assertEqual(put_request.status_code, 404)
        self.assertEqual(response['message'], "There is no parcel with ID 100")

    def test_change_status_non_existent_parcel_delivery_order(self):       
        self.admin_login()
        put_request = self.app_client.put("/api/v1/parcels/100/status", data=json.dumps({"status":"cancelled"}), 
            headers={'Authorization': f"Bearer {self.admin_access_token}"})
        response = json.loads(put_request.data.decode())
        self.assertEqual(put_request.status_code, 404)
        self.assertEqual(response['message'], "There is no parcel with ID 100")

    # def test_change_status_wrong_value(self):       
    #     self.user_login()
    #     self.admin_login()
    #     post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
    #         headers={'Authorization': f"Bearer {self.user_access_token}"}, data=json.dumps(test_parcel))
    #     put_request = self.app_client.put("/api/v1/parcels/1/status", data=json.dumps({"status":"okay"}), 
    #         headers={'Authorization': f"Bearer {self.admin_access_token}"})
    #     response = json.loads(put_request.data.decode())
    #     self.assertEqual(put_request.status_code, 400)
    #     self.assertEqual(response['message'], "Status can only be ['pending', 'intransit', 'cancelled', 'delivered']")

    # def test_change_status_empty_value(self):       
    #     self.user_login()
    #     self.admin_login()
    #     post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
    #         headers={'Authorization': f"Bearer {self.user_access_token}"}, data=json.dumps(test_parcel))
    #     put_request = self.app_client.put("/api/v1/parcels/100/status", data=json.dumps({"status":""}), 
    #         headers={'Authorization': f"Bearer {self.admin_access_token}"})
    #     response = json.loads(put_request.data.decode())
    #     self.assertEqual(put_request.status_code, 400)
    #     self.assertEqual(response['message'], "Please enter a new value")

    # def test_change_status_int_value(self):       
    #     self.user_login()
    #     self.admin_login()
    #     post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
    #         headers={'Authorization': f"Bearer {self.user_access_token}"}, data=json.dumps(test_parcel))
    #     put_request = self.app_client.put("/api/v1/parcels/100/status", data=json.dumps({"status":90}), 
    #         headers={'Authorization': f"Bearer {self.admin_access_token}"})
    #     response = json.loads(put_request.data.decode())
    #     self.assertEqual(put_request.status_code, 400)
    #     self.assertEqual(response['message'], "The value must be a string")

    # def test_change_status_letters_value(self):       
    #     self.user_login()
    #     self.admin_login()
    #     post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
    #         headers={'Authorization': f"Bearer {self.user_access_token}"}, data=json.dumps(test_parcel))
    #     put_request = self.app_client.put("/api/v1/parcels/100/status", data=json.dumps({"status":"90"}), 
    #         headers={'Authorization': f"Bearer {self.admin_access_token}"})
    #     response = json.loads(put_request.data.decode())
    #     self.assertEqual(put_request.status_code, 400)
    #     self.assertEqual(response['message'], "The value must be letters")


    def test_present_location_empty_value(self):       
        self.user_login()
        self.admin_login()
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
            headers={'Authorization': f"Bearer {self.user_access_token}"}, data=json.dumps(test_parcel))
        put_request = self.app_client.put("/api/v1/parcels/1/present_location", data=json.dumps({"present_location":""}), 
            headers={'Authorization': f"Bearer {self.admin_access_token}"})
        response = json.loads(put_request.data.decode())
        self.assertEqual(put_request.status_code, 400)
        self.assertEqual(response['message'], "Please enter a new value")

    # def test_present_location_int_value(self):       
    #     self.user_login()
    #     self.admin_login()
    #     post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
    #         headers={'Authorization': f"Bearer {self.user_access_token}"}, data=json.dumps(test_parcel))
    #     put_request = self.app_client.put("/api/v1/parcels/1/present_location", data=json.dumps({"present_location":90}), 
    #         headers={'Authorization': f"Bearer {self.admin_access_token}"})
    #     response = json.loads(put_request.data.decode())
    #     self.assertEqual(put_request.status_code, 400)
    #     self.assertEqual(response['message'], "The value must be a string")

    def test_change_present_location_letters_value(self):       
        self.user_login()
        self.admin_login()
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
            headers={'Authorization': f"Bearer {self.user_access_token}"}, data=json.dumps(test_parcel))
        put_request = self.app_client.put("/api/v1/parcels/1/present_location", data=json.dumps({"present_location":"90"}), 
            headers={'Authorization': f"Bearer {self.admin_access_token}"})
        response = json.loads(put_request.data.decode())
        self.assertEqual(put_request.status_code, 400)
        self.assertEqual(response['message'], "The value must be letters")


    def test_destination_empty_value(self):       
        self.user_login()
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
            headers={'Authorization': f"Bearer {self.user_access_token}"}, data=json.dumps(test_parcel))
        put_request = self.app_client.put("/api/v1/parcels/1/destination", data=json.dumps({"destination":""}), 
            headers={'Authorization': f"Bearer {self.user_access_token}"})
        response = json.loads(put_request.data.decode())
        self.assertEqual(put_request.status_code, 400)
        self.assertEqual(response['message'], "Please enter a new value")

    # def test_destination_int_value(self):       
    #     self.user_login()
    #     post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
    #         headers={'Authorization': f"Bearer {self.user_access_token}"}, data=json.dumps(test_parcel))
    #     put_request = self.app_client.put("/api/v1/parcels/1/destination", data=json.dumps({"destination":90}), 
    #         headers={'Authorization': f"Bearer {self.user_access_token}"})
    #     response = json.loads(put_request.data.decode())
    #     self.assertEqual(put_request.status_code, 400)
    #     self.assertEqual(response['message'], "The value must be a string")

    def test_change_destination_letters_value(self):       
        self.user_login()
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
            headers={'Authorization': f"Bearer {self.user_access_token}"}, data=json.dumps(test_parcel))
        put_request = self.app_client.put("/api/v1/parcels/1/destination", data=json.dumps({"destination":"90"}), 
            headers={'Authorization': f"Bearer {self.user_access_token}"})
        response = json.loads(put_request.data.decode())
        self.assertEqual(put_request.status_code, 400)
        self.assertEqual(response['message'], "The value must be letters")


    

    def test_wrong_user_change_present_location(self):     
        self.user_login()
        self.user2_login()
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
            headers={'Authorization': f"Bearer {self.user_access_token}"}, data=json.dumps(test_parcel))
        put_request = self.app_client.put("/api/v1/parcels/1/present_location", data=json.dumps({"present_location":"masaka"}), 
            headers={'Authorization': f"Bearer {self.user_access_token2}"})
        response = json.loads(put_request.data.decode())
        self.assertEqual(put_request.status_code, 401)
        self.assertEqual(response['message'], "Invalid request! You do not have rights to change the present location of a parcel")

    def test_wrong_user_change_status(self):
        self.user_login()
        self.user2_login()
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
            headers={'Authorization': f"Bearer {self.user_access_token}"}, data=json.dumps(test_parcel))
        put_request = self.app_client.put("/api/v1/parcels/1/status", data=json.dumps({"status":"cancelled"}), 
            headers={'Authorization': f"Bearer {self.user_access_token2}"})
        response = json.loads(put_request.data.decode())
        self.assertEqual(put_request.status_code, 401)
        self.assertEqual(response['message'], "Invalid request! You do not have rights to change the status of parcel 1")

    def test_wrong_user_change_destination(self):
        self.user_login()
        self.user2_login()
        post_request = self.app_client.post("/api/v1/parcels", content_type='application/json', 
            headers={'Authorization': f"Bearer {self.user_access_token}"}, data=json.dumps(test_parcel))
        put_request = self.app_client.put("/api/v1/parcels/1/destination", 
            data=json.dumps({"destination":"masaka"}), headers={'Authorization': f"Bearer {self.user_access_token2}"})
        response = json.loads(put_request.data.decode())
        self.assertEqual(put_request.status_code, 401)
        self.assertEqual(response['message'], "Invalid request! You do not have rights to change the destination of a parcel")


if __name__ == ('__main__'):
    unittest.main()