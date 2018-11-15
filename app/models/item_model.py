import json
from flask import jsonify

class Item:
    
    def __init__(self, item_name, item_weight):
        self.item_name = item_name
        self.item_weight = item_weight

    def get_unit_delivery_price(item_weight):
        if item_weight<500:
            unit_delivery_price = 1000
        elif 501<item_weight<1000:
            unit_delivery_price = 10000
        else: 
            unit_delivery_price = 100000
        return unit_delivery_price
    
    def get_amount(weight,delivery_price):
        amount = weight * delivery_price
        return amount

    def to_dictionary(self):
        return {
            "item_name": self.item_name,
            "item_weight": self.item_weight,
            "unit_delivery_price": Item.get_unit_delivery_price(self.item_weight),
            "amount":Item.get_amount(self.item_weight,Item.get_unit_delivery_price(self.item_weight))
        }