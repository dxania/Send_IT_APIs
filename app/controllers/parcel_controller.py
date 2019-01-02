import re
import json
from flask import jsonify, request
from flask_jwt_extended import (create_access_token, get_jwt_identity)
from app import app
from app.models.parcel_model import Parcel
from app.models.users_model import *
from app.validator import Validator
from app.controllers.db import DatabaseConnection

db = DatabaseConnection()

class Parcel_Controller:

    def index():
        """Index page"""
        return """parcels ==>
        <a href="https://send-it-api-app.herokuapp.com/api/v1/parcels">
        Navigate to this link to interact with the API</a><br><br>
        """

    def get_parcels():
        """Retrieve all parcels"""     
        parcel_list = []
        current_user = get_jwt_identity()
        if current_user.get('role') == True:
            parcels = db.get_all_parcels()
            if len(parcels) >= 1:
                for parcel in parcels:
                    parcel_dict = Parcel.to_dict(parcel)
                    parcel_list.append(parcel_dict)
                return jsonify({"parcels": parcel_list}), 200
            return jsonify({'message':'There are no parcel delivery orders'}), 200
        return jsonify({'message':'You can only view parcels you created'}), 401

    def get_parcels_by_user(user_id):
        """Retrieve all parcels by a specific user"""
        parcel_list = []
        current_user = get_jwt_identity()
        if current_user.get('id') == user_id or current_user.get('role') == True:
            parcels = db.get_parcels_by_user(user_id)
            if len(parcels) >= 1:
                for parcel in parcels:
                    parcel_dict = Parcel.to_dict(parcel)
                    parcel_list.append(parcel_dict)
                return jsonify({"parcels": parcel_list}), 200
            return jsonify({'message':f"There are no parcels delivery orders created by user {user_id}"}), 200
        return jsonify({'message':'You can only view parcels you created'}), 401

    def get_delivered_parcels_by_user(user_id):
        """Retrieve all parcels by a specific user"""
        parcel_list = []
        current_user = get_jwt_identity()
        if current_user.get('id') == user_id:
            parcels = db.get_user_parcels_by_status(user_id, 'delivered')
            if len(parcels) >= 1:
                for parcel in parcels:
                    parcel_dict = Parcel.to_dict(parcel)
                    parcel_list.append(parcel_dict)
                return jsonify({"parcels": parcel_list}), 200
            return jsonify({'message':f"There are no parcels delivery orders created by user {user_id}"}), 200
        return jsonify({'message':'You can only view parcels you created'}), 401

    # def get_intransit_parcels_by_user(user_id):
    #     """Retrieve all parcels by a specific user"""
    #     parcel_list = []
    #     current_user = get_jwt_identity()
    #     if current_user.get('id') == user_id:
    #         parcels = db.get_user_parcels_by_status(user_id, 'intransit')
    #         if len(parcels) >= 1:
    #             for parcel in parcels:
    #                 parcel_dict = Parcel.to_dict(parcel)
    #                 parcel_list.append(parcel_dict)
    #             return jsonify({"parcels": parcel_list}), 200
    #         return jsonify({'message':f"There are no parcels delivery orders created by user {user_id}"}), 200
    #     return jsonify({'message':'You can only view parcels you created'}), 401

    # def get_pending_parcels_by_user(user_id):
    #     """Retrieve all parcels by a specific user"""
    #     parcel_list = []
    #     current_user = get_jwt_identity()
    #     if current_user.get('id') == user_id:
    #         parcels = db.get_user_parcels_by_status(user_id, 'pending')
    #         if len(parcels) >= 1:
    #             for parcel in parcels:
    #                 parcel_dict = Parcel.to_dict(parcel)
    #                 parcel_list.append(parcel_dict)
    #             return jsonify({"parcels": parcel_list}), 200
    #         return jsonify({'message':f"There are no parcels delivery orders created by user {user_id}"}), 200
    #     return jsonify({'message':'You can only view parcels you created'}), 401

    # def get_cancelled_parcels_by_user(user_id):
    #     """Retrieve all parcels by a specific user"""
    #     parcel_list = []
    #     current_user = get_jwt_identity()
    #     if current_user.get('id') == user_id:
    #         parcels = db.get_user_parcels_by_status(user_id, 'cancelled')
    #         if len(parcels) >= 1:
    #             for parcel in parcels:
    #                 parcel_dict = Parcel.to_dict(parcel)
    #                 parcel_list.append(parcel_dict)
    #             return jsonify({"parcels": parcel_list}), 200
    #         return jsonify({'message':f"There are no parcels delivery orders created by user {user_id}"}), 200
    #     return jsonify({'message':'You can only view parcels you created'}), 401

    def get_parcel(parcel_id):
        """Retrieve a particular parcel"""
        current_user = get_jwt_identity()
        parcel = db.get_a_parcel(parcel_id)  
        if parcel:
            if current_user.get('role') == True or current_user.get('id') == parcel[2]:
                parcel_dict = Parcel.to_dict(parcel)
                return jsonify({"parcel":parcel_dict}), 200
            return jsonify({'message': f"You can only view parcels you created"}), 401
        return jsonify({'message': f"There is no parcel with ID {parcel_id}"}), 404
        

    def change_present_location(parcel_id):
        """Change the present location of a parcel delivery order"""
        current_user = get_jwt_identity()
        user_input = request.get_json(force=True) 
        parcel = db.get_a_parcel(parcel_id)
        if parcel:
            if current_user.get('role') == True:
                present_location = user_input.get('present_location')
                validated_location = Validator.validate_str_to_change(present_location)
                if validated_location:
                    return validated_location
                if parcel[10] == 'cancelled' or parcel[10] == 'delivered':  
                    return jsonify({"message":f"Present location of parcel {parcel_id} can not be changed because it was cancelled or delivered"}), 400 
                location_change = db.change_location(parcel_id, present_location)
                if location_change:
                    if present_location != parcel[7]:
                        db.change_status(parcel_id, 'intransit')
                    elif present_location == parcel[7]:
                        db.change_status(parcel_id, 'delivered')
                    return jsonify({"message":f"Present location of parcel {parcel_id} changed to {present_location}"}), 200
            return jsonify({'message':'Invalid request! You do not have rights to change the present location of a parcel'}), 401
        return jsonify({'message':f"There is no parcel with ID {parcel_id}"}), 404


    def change_parcel_destination(parcel_id):
        """Change the destination of a parcel delivery order"""
        current_user = get_jwt_identity()
        user_input = request.get_json(force=True) 
        parcel = db.get_a_parcel(parcel_id)
        if parcel:
            if current_user.get('id') == parcel[2]:
                destination = user_input.get('destination')
                price = user_input.get('total_price')
                validated_destination = Validator.validate_str_to_change(destination)
                if validated_destination:
                    return validated_destination   
                if parcel[10] == 'cancelled' or parcel[10] == 'delivered':  
                    return jsonify({"message":f"Destination of parcel {parcel_id} can not be changed because it was cancelled or delivered"}), 400
                destination_change = db.change_destination(parcel_id, destination, price)
                if destination_change:
                    return jsonify({"message":f"Destination of parcel {parcel_id} changed to {destination}"}), 200  
            return jsonify({'message':f"Invalid request! You do not have rights to change the destination of a parcel"}), 401 
        return jsonify({'message':f"There is no parcel with ID {parcel_id}"}), 404


    def change_parcel_status(parcel_id):
        """Change the status of a parcel delivery order"""
        current_user = get_jwt_identity()
        parcel = db.get_a_parcel(parcel_id)
        if parcel:
            if parcel[0] == parcel_id and current_user.get('id') == parcel[2]: 
                if parcel[10] != 'pending':
                    return jsonify({"message":f"Parcel {parcel_id} can not be cancelled"}), 400 
                status_change = db.change_status(parcel_id, 'cancelled')
                return jsonify({"message":f"Parcel {parcel_id} has been cancelled"}), 200  
            return jsonify({'message':f"Invalid request! You do not have rights to change the status of parcel {parcel_id}"}), 401 
        return jsonify({'message':f"There is no parcel with ID {parcel_id}"}), 404
        

    def create_parcel():
        """Create a parcel delivery order"""
        user_input = request.get_json(force=True)
        current_user = get_jwt_identity()
        # descriptions = ["Electronics", "Perishable goods", "Furniture", "Home appliances",
        #                 "Clothing", "Bags and shoes", "Toys"]  
        user_id = current_user.get('id')
        user_name = current_user.get('username')
        recipient_name = user_input.get("recipient_name")
        recipient_mobile = user_input.get("recipient_mobile")
        pickup_location = user_input.get("pickup_location")
        destination = user_input.get("destination")
        weight = user_input.get("weight")
        total_price = Parcel.get_delivery_price(weight)
        description = user_input.get("description")
        # if not description in descriptions:
        #     return jsonify({"message": f"Description can only be {descriptions}"}), 400

        parcel_dict = {
            "description": description,
            "recipient_name": recipient_name,
            "recipient_mobile": recipient_mobile,
            "pickup_location" : pickup_location,
            "destination": destination,
            "weight": weight,
            "total_price": total_price
        }
        validate_parcel = Validator.validate_parcel(parcel_dict)
        # if validate_parcel:
        #     return validate_parcel
        msgs_list = validate_parcel['message']
        if len(msgs_list) > 0:
            return jsonify(validate_parcel), 400
        parcel = Parcel(user_id, user_name, parcel_dict)
        db.add_parcel(parcel.description, parcel.user_id, parcel.user_name, parcel.recipient_name, parcel.recipient_mobile, pickup_location, parcel.destination, parcel.weight, parcel.total_price)
        return jsonify({"message":"Parcel delivery order successfully made"}), 201
