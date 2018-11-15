import re
from flask import jsonify, request
from app import app
from app.models.parcel_model import Parcel, parcels
from app.models.users_model import *
from app.models.item_model import Item
from app.validator import Validator


class Parcel_Controller:

    def index():
        """Index page"""
        return """parcels ==>
        <a href="https://send-it-api-app.herokuapp.com/api/v1/parcels">
        Navigate to this link to interact with the API</a><br><br>
        """

    def get_parcels():
        """Retrieve all parcels"""
        parcels_list = []
        for parcel in parcels:
            parcels_list.append(parcel.to_dict())
        if parcels_list:
            return jsonify({"number_of_parcel_delivery_orders":len(parcels_list)},{"parcels": parcels_list}), 200
        return jsonify({"message":"There are no parcel delivery orders"}), 200


    def get_parcels_by_user(user_id):
        """Retrieve all parcels by a specific user"""
        my_parcels = []
        for parcel in parcels:
            if parcel.to_dict()['user_id'] == user_id:
                my_parcels.append(parcel.to_dict())
        if my_parcels:
            return jsonify({"number_of_parcel_delivery_orders":len(my_parcels)},{'my_pacels':my_parcels}), 200
        return jsonify({'message':'There are no parcels delivery orders created by that user or the user does not exist'}), 200


    def get_parcel(parcel_id):
        """Retrieve a particular parcel"""
        for parcel in parcels:
            if parcel.to_dict()['parcel_id'] == parcel_id:
                return jsonify({"parcel":parcel.to_dict()}), 200
        return jsonify({'message': f"Parcel with ID {parcel_id} does not exist"}), 200


    def cancel_parcel(parcel_id):
        """Cancel a particular parcel delivery order"""
        for parcel in parcels:
            parcel_dict = parcel.to_dict()
            if parcel_dict['parcel_id'] == parcel_id: 
                parcel_dict["status"] = "cancelled"
                return jsonify({"Parcel_delivery_order_cancelled":parcel_dict}), 200
        return jsonify({'message':'There is no parcel with that ID'}), 200


    def cancel_parcel_by_user(parcel_id, user_id):
        """Cancel a particular parcel delivery order by a user"""
        for parcel in parcels:
            parcel_dict = parcel.to_dict()
            if parcel_dict['parcel_id'] == parcel_id and parcel_dict['user_id'] == user_id: 
                parcel_dict["status"] = "cancelled"
                return jsonify({"Parcel_delivery_order_cancelled":parcel_dict}), 200
            return jsonify({'message':'You dont have rights to cancel this parcel delivery order'}), 200
        return jsonify({'message':'There is no parcel with that ID'}), 200


    def create_parcel():
        """Create a parcel delivery order"""
        user_input = request.get_json(force=True)

        user_id = user_input.get("user_id")
        destination = user_input.get("destination")
        recipient_name = user_input.get("recipient_name")
        recipient_mobile = user_input.get("recipient_mobile")
        pickup_location = user_input.get("pickup_location")
        result_items = user_input.get("items")

        items = []
        if not result_items or not isinstance(result_items, list):
            return jsonify({'message':'Please enter atleast one item; Items must be a list of dictionaries'}), 400
        else:
            for result_item in result_items:
                item_name = result_item.get("item_name")
                item_weight = result_item.get('item_weight')

                validator = Validator.validate_item(result_item)
                if len(validator) > 0:
                    return jsonify({'errors':validator}), 400
                item = Item(item_name , item_weight)
                items.append(item) 

        parcel_dict = {
            "user_id": user_id,
            "recipient_name": recipient_name,
            "recipient_mobile": recipient_mobile,
            "pickup_location" : pickup_location,
            "destination": destination
        }
        validate_parcel = Validator.validate_parcel(parcel_dict)
        if len(validate_parcel) > 0:
            return jsonify({'errors':validate_parcel}), 400
        parcel = Parcel(parcel_dict, items)

        for user in users:
            user_dict = user.to_dict()
            if user_dict['user_id'] == user_id:
                parcels.append(parcel)
                return jsonify({"parcel_successfully_created":parcel.to_dict()}), 201
        return jsonify({'message':'You dont have rights to create a parcel delivery order'}), 200