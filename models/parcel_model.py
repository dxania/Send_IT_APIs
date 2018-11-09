import json
from flask import jsonify
from users_model import users

parcels = []
instance_Items = []
status = ['delivered', 'pending', 'cancelled']


class Items:
    
    def __init__(self, item_name, item_weight, unit_delivery_price):
        self.item_name = item_name
        self.item_weight = item_weight
        self.unit_delivery_price = unit_delivery_price
        self.amount = item_weight * unit_delivery_price
    
    def create_item(self):
        item = {
            "item_name": self.item_name, 
            "weight": self.weight, 
            "unit_delivery_price": self.unit_delivery_price, 
            "amount": self.amount
        }
        
        instance_Items.append(item)
        return item
        # for item in items:
        #     if item['name'] == item_name:
        #         return jsonify({'message':'You have already added that item'})
        #     else:
                

    # def get_total_amount(self):

        

an_item = Items(item_name, item_weight, unit_delivery_price)
the_item = an_item.create_item()

for item in instance_Items:
    total_Weight = item['weight']
    total_Weight += item['weight']
    total_Price = item['amount']
    total_Price += item['amount']

class Parcel():
    """Parcels class defining 
    the parcel model
    """
    def __init__(self, user_id, parcel_id, pickup_location, destination, items):
        self.user_id = user_id
        self.parcel_id = len(parcels) + 1
        self.pickup_location = pickup_location
        self.destination = destination
        self.no_of_items = len(instance_Items)
        self.items = instance_Items
        self.total_weight = total_Weight
        self.total_price = total_Price
        self.parcel_status = "pending"

        
    def create_a_parcel(self):
 
        parcel = {
            "user_id": self.user_id,
            "parcel_id" : self.parcel_id,
            "pickup_location" : self.pickup_location,
            "destination": self.destination,
            "no_of_items": self.no_of_items,
            "items": self.items,
            "total_weight":self.total_weight,
            "total_price": self.total_price,
            "status":self.parcel_status
        }

        for user in users:
            # for parcelStatus in status:
            # if user_id and parcelStatus:
            if user_id:
                parcels.append(parcel)
                return jsonify({"parcel successfully created":parcel})
            else:
                return({'message':'you dont have rights to create a parcel'})

    @staticmethod
    def get_all_parcels():
        """Method to get and 
        return all parcels
        """
        # if len(parcels) > 0:
        return jsonify({"parcels": parcels})

    @staticmethod
    def get_all_parcels_by_user(user_id):
        """Method to get and 
        return all parcels
        created by a specific user
        """
        for user in users:
            if user_id and len(parcels) > 0:
                for parcel in parcels:
                    if parcel['user_id'] == user_id:
                        return jsonify({"parcels": parcel})

    @staticmethod
    def get_a_parcel(parcel_id):
        """Method to get and return 
        a particular parcel
        """
        for parcel in parcels:
            if parcel['parcel_id'] == parcel_id:
                return jsonify(parcel)

    
    def cancel_parcel_delivery_order(parcel_id, user_id):
        # for user in users:
        #     if user_id and len(parcels) > 0:
        for parcel in parcels:
            if parcel['parcel_id'] == parcel_id and parcel['user_id'] == user_id and parcel['status'] == 'pending':
                parcel["status"] == "cancelled"
                # parcel = {
                #     "user_id": self.user_id,
                #     "parcel_id" : self.parcel_id,
                #     "pickup_location" : self.pickup_location,
                #     "destination": self.destination,
                #     "no_of_items": self.no_of_items,
                #     "items": self.items,
                #     "total_weight":self.total_weight,
                #     "total_price": self.total_price,
                #     "status":self.parcel_status
                # }
                parcels.append(parcel)
                return jsonify({"Parcel delivery order cancelled":parcel})
            else:
                return({'message':'you dont have rights to modify that parcel'})

            #     for parcelStatus in status:
            #         if parcelStatus:
            #             parcels.append(parcel)
            #             return jsonify({"Parcel delivery order cancelled":parcel})
            #         else:
            #             return jsonify({'message':'Please enter a valid status, "cancelled".'})
            # else:
            #     return({'message':'you dont have rights to modify that parcel'})
            # else:
            #     return({'message':'there is no user with that ID and therefore no parcel created by them'})

   

