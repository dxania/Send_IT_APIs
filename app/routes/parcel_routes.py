import re
from flask import jsonify, flash, request, make_response
from app import app
from app.models.parcel_model import Parcel, parcels
from app.models.users_model import *
from app.models.item_model import Item
from app.controllers.parcel_controller import Parcel_Controller


@app.route('/')
def index():
    """Index page"""
    return Parcel_Controller.index()

@app.route("/api/v1/parcels", methods = ['GET'])
def get_parcels():
    """Retrieve all parcels"""
    return Parcel_Controller.get_parcels()


@app.route("/api/v1/users/<int:user_id>/parcels", methods = ['GET'])
def get_parcels_by_user(user_id):
    """Retrieve all parcels by a specific user"""
    return Parcel_Controller.get_parcels_by_user(user_id)


@app.route('/api/v1/parcels/<int:parcel_id>', methods = ['GET'])
def get_parcel(parcel_id):
    """Retrieve a particular parcel"""
    return Parcel_Controller.get_parcel(parcel_id)


@app.route('/api/v1/parcels/<int:parcel_id>/cancel', methods = ['PUT'])
def cancel_parcel(parcel_id):
    """Cancel a particular parcel delivery order"""
    for parcel in parcels:
        parcel_dict = parcel.to_dict()
        if parcel_dict['parcel_id'] == parcel_id: 
            if parcel_dict['status'] == 'pending':
                parcel_dict["status"] = "cancelled"
                return jsonify({"Parcel_delivery_order_cancelled":parcel_dict}), 200
            else:
                return jsonify({'message':'The parcel delivery order is not pending! It cannot be cancelled'}), 200
    return jsonify({'message':'There is no parcel with that ID'}), 200



@app.route('/api/v1/users/<int:user_id>/<int:parcel_id>/cancel', methods = ['PUT'])
def cancel_parcel_by_user(parcel_id, user_id):
    """Cancel a particular parcel delivery order by a user"""
    for parcel in parcels:
        parcel_dict = parcel.to_dict()
        if parcel_dict['parcel_id']:
            if parcel_dict['parcel_id'] == parcel_id and parcel_dict['user_id'] == user_id: 
                if parcel_dict['status'] == 'pending':
                    parcel_dict["status"] = "cancelled"
                    return jsonify({"Parcel_delivery_order_cancelled":parcel_dict}), 200
                else:
                    return jsonify({'message':'The parcel delivery order is not pending! It cannot be cancelled'}), 200
            else:
                return jsonify({'message':'You dont have rights to cancel this parcel delivery order'}), 200
    return jsonify({'message':'There is no parcel with that ID'}), 200

   
@app.route('/api/v1/parcels', methods =['POST'])
def create_parcel():
    """Create a parcel function wrapped around the Post /parcels endpoint"""
    user_input = request.get_json(force=True)

 
    user_id = user_input.get("user_id")
    if not isinstance(user_id, int):
        return jsonify({'message':'Enter a valid user ID'}), 400
    if not user_id:
        return jsonify({'message':'User ID is required'}), 400

    destination = user_input.get("destination")
    if not destination or destination.isspace():
        return jsonify({'message':'Destination is required'}), 400
    charset = re.compile('[A-Za-z]')
    checkmatch = charset.match(destination)
    if not checkmatch:
        return jsonify({'message':'Destination must be letters'}), 400

    pickup_location = user_input.get("pickup_location")
    if not pickup_location or pickup_location.isspace():
        return jsonify({'message':'Pickup location is required'}), 400
    charset = re.compile('[A-Za-z]')
    checkmatch = charset.match(pickup_location)
    if not checkmatch:
        return jsonify({'message':'Pickup location must be letters'}), 400

    result_items = user_input.get("items")
    if not result_items:
        return jsonify({'message':'Enter at least one item'}), 400
    if not isinstance(result_items, list):
        return jsonify({'message':'Items must be a list of dictionaries'}), 400
    
    parcel_id = len(parcels) + 1

    
    items = []
    for result_item in result_items:
        item_name = result_item["item_name"] 
        if not item_name or item_name.isspace():
            return jsonify({'message':'Parcel item name is required'}), 400
        charset = re.compile('[A-Za-z]')
        checkmatch = charset.match(item_name)
        if not checkmatch:
            return jsonify({'message':'Parcel item name must be letters'}), 400

        item_weight = result_item['item_weight'] 
        if not item_weight:
            return jsonify({'message':'Parcel item weight is required'}), 400
        if not isinstance(item_weight,int):
            return jsonify({'message':'Parcel item weight must be an integer'}), 400
    
    
        unit_delivery_price = result_item['unit_delivery_price']
        if not unit_delivery_price:
            return jsonify({'message':'Parcel item unit delivery price is required'}), 400
        if not isinstance(unit_delivery_price,int):
            return jsonify({'message':'Parcel item unit delivery price must be an integer'}), 400
            
        item = Item(item_name, item_weight, unit_delivery_price)
        items.append(item)

    parcel = Parcel(user_id, parcel_id, pickup_location, destination, items)

    # try:
    for user in users:
        user_dict = user.to_dict()
        if user_dict['user_id'] == user_id:
            parcels.append(parcel)
            return jsonify({"parcel_successfully_created":parcel.to_dict()}), 201
    # except Exception as e:
    #     print(e.message)
    return jsonify({'message':'You dont have rights to create a parcel delivery order'}), 200