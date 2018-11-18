import json
from flask import jsonify
from app.models.users_model import users

parcels = []
class Parcel():
    """Parcels class defining the parcel model"""
    def __init__(self, user_id, parcel, items):
        self.user_id = user_id
        self.parcel_id = len(parcels) + 1
        self.pickup_location = parcel['pickup_location']
        self.destination = parcel['destination']
        self.instance_Items = items
        self.parcel_status = "pending"
        self.recipient_name = parcel['recipient_name']
        self.recipient_mobile = parcel['recipient_mobile']


    def get_total(self, variable):
        items = []
        for item in self.instance_Items:
            an_item = item.to_dictionary()
            items.append(an_item)
            total_price = sum([an_item[variable] for an_item in items])
        return total_price
 

    def to_dict(self):
        items = []

        for item in self.instance_Items:
            items.append(item.to_dictionary())
 
        parcel = {
            "created_by": self.user_id,
            "parcel_id" : self.parcel_id,
            "recipient_name": self.recipient_name,
            "recipient_mobile": self.recipient_mobile,
            "pickup_location" : self.pickup_location,
            "destination": self.destination,
            "no_of_items": len(self.instance_Items),
            "items": items,
            "total_weight":self.get_total('item_weight'),
            "total_price": self.get_total('amount'),
            "status":self.parcel_status
        }

        return parcel