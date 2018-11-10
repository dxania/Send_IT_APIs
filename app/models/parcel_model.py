import json
from flask import jsonify
from app.models.users_model import users

parcels = []
instance_Items = []
status = ['delivered', 'pending', 'cancelled']


class Items:
    instance_Items = []
    def __init__(self, item_name, item_weight, unit_delivery_price):
        self.item_name = item_name
        self.item_weight = item_weight
        self.unit_delivery_price = unit_delivery_price
        # self.instance_Items = []
        # self.amount = self.item_weight * self.unit_delivery_price
    
    def create_item(self):
        # self.instance_Items = []
        item = {
            "item_name": self.item_name, 
            "weight": self.item_weight, 
            "unit_delivery_price": self.unit_delivery_price, 
            # "amount": self.amount
        }
        # Items.instance_Items.append(item)
        # instance_Items.append(item)
        # return item
        # for item in items:
        #     if item['name'] == item_name:
        #         return jsonify({'message':'You have already added that item'})
        # 
           
    # @staticmethod
    # def get_total_weight(items_list):
    #     for item in instance_Items:
    #         total_Weight = item['weight']
            # total_Weight += item['weight']
            # total_Price = item['amount']
            # total_Price += item['amount']

        # return total_Weight
# an_item = Items(item_name, item_weight, unit_delivery_price)
# an_item.instance_Items
# the_item = Items(**args)
# the_item = an_item.create_item()

# for item in instance_Items:
#     total_Weight = item['weight']
#     total_Weight += item['weight']
#     total_Price = item['amount']
#     total_Price += item['amount']


class Parcel():
    """Parcels class defining 
    the parcel model
    """
    def __init__(self, user_id, parcel_id, pickup_location, destination, items):
        self.user_id = user_id
        self.parcel_id = len(parcels) + 1
        self.pickup_location = pickup_location
        self.destination = destination
        self.no_of_items = len(Items.instance_Items)
        self.items = instance_Items
        # self.total_weight = Items.get_total_weight(self.items)
        # self.total_price = total_Price
        self.parcel_status = "pending"

        
    def create_a_parcel(self):
 
        parcel = {
            "user_id": self.user_id,
            "parcel_id" : self.parcel_id,
            "pickup_location" : self.pickup_location,
            "destination": self.destination,
            "no_of_items": self.no_of_items,
            "items": self.items,
            # "total_weight":self.total_weight,
            # "total_price": self.total_price,
            "status":self.parcel_status
        }

        for user in users:
            # if user['user_id'] == user_id:
            if user["user_id"]:
                parcels.append(parcel)
                return jsonify({"parcel successfully created":parcel})
            else:
                return({'message':'you dont have rights to create a parcel'})

    @staticmethod
    def get_all_parcels():
        """Method to get and 
        return all parcels
        """
        if len(parcels) > 0:
            return jsonify({"parcels": parcels})

    @staticmethod
    def get_all_parcels_by_user(user_id):
        """Method to get and 
        return all parcels
        created by a specific user
        """
        # for user in users:
        #     if user_id and len(parcels) > 0:
        my_parcels = []
        for parcel in parcels:
            if parcel['user_id'] == user_id:
                my_parcels.append(parcel)
        
        if len(my_parcels) > 0:
            return jsonify(my_parcels)

    @staticmethod
    def get_a_parcel(parcel_id):
        """Method to get and return 
        a particular parcel
        """
        for parcel in parcels:
            if parcel['parcel_id'] == parcel_id:
                return jsonify(parcel)

    
    def cancel_parcel_delivery_order(parcel_id, user_id):
        """Method to cancel a parcel 
        delivery order and change 
        status to cancelled
        """
        for parcel in parcels:
            if parcel['parcel_id'] == parcel_id and parcel['user_id'] == user_id and parcel['status'] == 'pending':
                parcel["status"] = "cancelled"
                return jsonify({"Parcel delivery order cancelled":parcel})
            else:
                return({'message':'you dont have rights to modify that parcel'})


   

