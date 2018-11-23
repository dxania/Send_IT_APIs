import json
from flask import jsonify
from app.models.users_model import users

class Parcel():
    """Parcels class defining the parcel model"""
    def __init__(self, user_id, parcel):    
        self.user_id = user_id
        self.pickup_location = parcel['pickup_location']
        self.destination = parcel['destination']
        self.recipient_name = parcel['recipient_name']
        self.recipient_mobile = parcel['recipient_mobile']
        self.weight = parcel['weight']
        self.total_price = parcel['total_price']

    @staticmethod
    def get_delivery_price(weight):
        if isinstance(weight, int):
            if weight<500:
                delivery_price = 10000
            elif 501<weight<1000:
                delivery_price = 100000
            else: 
                delivery_price = 1000000
            return delivery_price

    @staticmethod
    def to_dict(parcel):
        parcel_dict = {
            "parcel_id": parcel[0],
            "created_by": parcel[2],
            "recipient_name": parcel[3],
            "recipient_mobile": parcel[4],
            "pickup_location" : parcel[5],
            "destination": parcel[6],
            "weight": parcel[7],
            "total_price":parcel[8],
            "status": parcel[9],
            "present_location": parcel[10]
        }
        return parcel_dict