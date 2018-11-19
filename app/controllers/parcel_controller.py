import re
import json
from flask import jsonify, request
from flask_jwt_extended import (create_access_token, get_jwt_identity)
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
        current_user = get_jwt_identity()
        if current_user == 'admin':
            for parcel in parcels:
                parcels_list.append(parcel.to_dict())
            if len(parcels_list) > 0:
                return jsonify({"number_of_parcel_delivery_orders":len(parcels_list), "parcels": parcels_list}), 200
            return jsonify({"message":"There are no parcel delivery orders"}), 200
        return jsonify({'message':'Invalid request! login or use the right access token'})


    def get_parcels_by_user(user_id):
        """Retrieve all parcels by a specific user"""
        current_user = get_jwt_identity()
        my_parcels = []
        char_set = re.compile('[A-Za-z]')
        if not char_set.match(user_id):
            return jsonify({'message':'Enter a valid user name'}), 200
        for parcel in parcels:
            if parcel.to_dict()['created_by'] == user_id:
                my_parcels.append(parcel.to_dict())
        if current_user == 'admin' or current_user == user_id:
            if len(my_parcels) > 0:
                return jsonify({"number_of_parcel_delivery_orders":len(my_parcels), "my_pacels":my_parcels}), 200
            return jsonify({'message':f"There are no parcels delivery orders created by {user_id}"}), 200
        return jsonify({'message':'Invalid request! login or use the right access token'}), 400


    def get_parcel(parcel_id):
        """Retrieve a particular parcel"""
        current_user = get_jwt_identity()
        for parcel in parcels:
            if current_user == 'admin' or current_user == parcel.to_dict()['created_by']:
                if parcel.to_dict()['parcel_id'] == parcel_id:
                    return jsonify({"parcel":parcel.to_dict()}), 200
            return jsonify({'message': f"You do not have access to parcel delivery order {parcel_id}"}), 400
        return jsonify({'message': f"Parcel with ID {parcel_id} does not exist"}), 200


    def change_present_location(parcel_id):
        """Change the present location of a parcel delivery order"""
        current_user = get_jwt_identity()
        if current_user == 'admin':
            user_input = request.get_json(force=True)
            for parcel in parcels:
                parcel_dict = parcel.to_dict()
                if parcel_dict['parcel_id'] == parcel_id:
                    parcel_dict.update({"present_location":user_input.get('present_location')})
                    return jsonify({"Present_location_changed":parcel_dict}), 200
            return jsonify({'message':'There is no parcel with that ID'}), 200
        return jsonify({'message':'Invalid request! login or use the right access token'}), 400

    def change_parcel_destination(parcel_id):
        """Change the destination of a parcel delivery order"""
        current_user = get_jwt_identity()
        user_input = request.get_json(force=True)
        for parcel in parcels:
            parcel_dict = parcel.to_dict()
            if parcel_dict['parcel_id'] == parcel_id and current_user == parcel_dict['created_by']:  
                parcel_dict.update({"destination":user_input.get('destination')})
                return jsonify({"Destination_location_changed":parcel_dict}), 200
            return jsonify({'message':f"Invalid request! You do not have rights to change the destination of parcel {parcel_id}"}), 400
        return jsonify({'message':'There is no parcel with that ID'}), 200

    def cancel_parcel(parcel_id):
        """Cancel a particular parcel delivery order"""
        current_user = get_jwt_identity()
        if current_user == 'admin':
            for parcel in parcels:
                parcel_dict = parcel.to_dict()
                if parcel_dict['parcel_id'] == parcel_id:
                    parcel_dict.update({"status":"cancelled"})
                    return jsonify({"Parcel_delivery_order_cancelled":parcel_dict}), 200
            return jsonify({'message':'There is no parcel with that ID'}), 200
        return jsonify({'message':'Invalid request! login or use the right access token'}), 400


    def create_parcel():
        """Create a parcel delivery order"""
        user_input = request.get_json(force=True)

        current_user = get_jwt_identity()
        user_id = current_user
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
                msgs_list = validator['message(s)']
                if len(msgs_list) > 0:
                    return jsonify(validator), 400
                item = Item(item_name , item_weight)
                items.append(item) 

        parcel_dict = {
            "recipient_name": recipient_name,
            "recipient_mobile": recipient_mobile,
            "pickup_location" : pickup_location,
            "destination": destination
        }
        validate_parcel = Validator.validate_parcel(parcel_dict)
        msgs_list = validate_parcel['message(s)']
        if len(msgs_list) > 0:
            return jsonify(validate_parcel), 400
        parcel = Parcel(user_id, parcel_dict, items)

        if user_id:
            parcels.append(parcel)
            return jsonify({"parcel_successfully_created":parcel.to_dict()}), 201
        return jsonify({'message':'You dont have rights to create a parcel delivery order'}), 200