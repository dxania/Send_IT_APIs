import json
from flask import jsonify

class Item:
    
    def __init__(self, item_name, item_weight, unit_delivery_price):
        self.item_name = item_name
        self.item_weight = item_weight
        self.unit_delivery_price = unit_delivery_price

    def get_amount(weight,delivery_price):
        amount = weight * delivery_price
        return amount

    def to_dict(self):
        return {
            "item_name": self.item_name,
            "item_weight": self.item_weight,
            "unit_delivery_price": self.unit_delivery_price,
            "amount":Item.get_amount(self.item_weight,self.unit_delivery_price)
        }