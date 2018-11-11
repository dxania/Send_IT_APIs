import json
from flask import jsonify
from app.models.users_model import users

parcels = []

class Parcel():
    """Parcels class defining the parcel model"""
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