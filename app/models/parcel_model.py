import json
from flask import jsonify
from app.models.users_model import users
# from app.exception_handler import InvalidUsage

parcels = []

class Parcel():
    """Parcels class defining 
    the parcel model
    """
    def __init__(self, user_id, parcel_id, pickup_location, destination, items):
        self.user_id = user_id
        self.parcel_id = len(parcels) + 1
        self.pickup_location = pickup_location
        self.destination = destination
        self.instance_Items = items
        self.parcel_status = "pending"

    def get_total_weight(self):
        items = []
        for item in self.instance_Items:
            an_item = item.to_dict()
            items.append(an_item)
            weight = sum([an_item['item_weight'] for an_item in items])
        return weight

    def get_total_price(self):
        items = []
        for item in self.instance_Items:
            an_item = item.to_dict()
            items.append(an_item)
            total_price = sum([an_item['amount'] for an_item in items])
        return total_price
 

    def to_dict(self):
        items = []

        for item in self.instance_Items:
            items.append(item.to_dict())
 
        parcel = {
            "user_id": self.user_id,
            "parcel_id" : self.parcel_id,
            "pickup_location" : self.pickup_location,
            "destination": self.destination,
            "no_of_items": len(self.instance_Items),
            "items": items,
            "total_weight":self.get_total_weight(),
            "total_price": self.get_total_price(),
            "status":self.parcel_status
        }

        return parcel

    
    def cancel_parcel(parcel_id):
        """Method to cancel a parcel delivery order and change status to cancelled"""
        for parcel in parcels:
            if parcel['parcel_id'] == parcel_id: 
                if parcel['status'] == 'pending':
                    parcel["status"] = "cancelled"
                    return jsonify({"Parcel_delivery_order_cancelled":parcel})
                else:
                    return jsonify({'message':'The parcel delivery order is not pending! It cannot be cancelled'}), 400
            else:
                return jsonify({'message':'There is no parcel with that ID'}), 400
    
    
    def cancel_parcel_by_user(parcel_id, user_id):
        """Method to cancel a parcel delivery order by a user and change status to cancelled"""
        for parcel in parcels:
            if parcel['parcel_id'] == parcel_id and parcel['user_id'] == user_id and parcel['status'] == 'pending':
                parcel["status"] = "cancelled"
                return jsonify({"Parcel_delivery_order_cancelled":parcel})
            else:
                return jsonify ({'message':'You dont have rights to modify that parcel'})


   

