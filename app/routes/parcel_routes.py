import re

from flask import jsonify, flash, request, make_response

from app.exception_handler import InvalidUsage
from app import app
from app.models.parcel_model import Parcel, parcels, Items
from app.models.users_model import users

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    """Error handling and exception raising"""
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/')
def index():
    """The first page and endpoint that 
    is rendered on loading the url
    """
    return """parcels ==>
    <a href="">
    Navigate to this link to interact with the parcels endpoint</a><br><br>
    """


@app.route("/api/v1/parcels", methods = ['GET'])
def get_parcels():
    """Retrieve all parcels function 
    wrapped around the Get /parcels endpoint
    """
    all_parcels = Parcel.get_all_parcels()
    if all_parcels:
        return all_parcels, 200
    else:
        raise InvalidUsage('There are no parcels in the store', status_code=204) 

@app.route("/api/v1/users/<int:user_id>/parcels", methods = ['GET'])
def get_parcels_by_user(user_id):
    """Retrieve all parcels by a specific 
    user function wrapped around the 
    Get /parcels endpoint
    """
    all_parcels_by_user = Parcel.get_all_parcels_by_user(user_id)
    if all_parcels_by_user:
        return all_parcels_by_user, 200
    else:
        raise InvalidUsage('There are no parcels delivery orders created by that user', status_code=404)


@app.route('/api/v1/parcels/<int:parcel_id>', methods = ['GET'])
def get_parcel(parcel_id):
    """Retrieve a particular parcel 
    function wrapped around the Get 
    /parcel/<int:parcel_id> endpoint
    """
    a_single_parcel = Parcel.get_a_parcel(parcel_id)
    if a_single_parcel:
        return a_single_parcel, 200
    else:
        raise InvalidUsage('There is no parcel matching that ID', status_code=204)

@app.route('/api/v1/users/<int:user_id>/<int:parcel_id>/cancel', methods = ['PUT'])
def cancel_parcel(parcel_id, user_id):
    """Cancel a particular parcel delivery order
    function wrapped around the Put
    /parcels/<int:user_id>/<int:parcel_id> endpoint
    """
    # for user in users:
    #     if not user_id:
    #         raise InvalidUsage('You dont have rights to cancel this parcel delivery order', status_code=400)
    #     else:
    a_single_parcel_to_cancel = Parcel.cancel_parcel_delivery_order(parcel_id, user_id)
    if a_single_parcel_to_cancel:
        return a_single_parcel_to_cancel, 202
    else:
        raise InvalidUsage('You dont have rights to cancel this parcel delivery order', status_code=400)


   
@app.route('/api/v1/parcels', methods =['POST'])
def create_parcel():
    """Create a parcel function 
    wrapped around the Post /parcels 
    endpoint
    """

    #store the request data in user_input variable
    user_input = request.get_json(force=True)

    #validate user input
   
    # total_price = 
    items = user_input.get("items")
    if not items or len(items) == 0:
        raise InvalidUsage('Enter at least one item', status_code=400)
    if not isinstance(items, list):
        raise InvalidUsage('Items must be a list of dictionaries', status_code=400)
    

    # total_weight = Items.get_total_weight(items)
    # no_of_items = len(items)

    user_id = user_input.get("user_id")
    # for user in users:
    #     if user_id:
    #         raise InvalidUsage('That user id does not exist, you cannot create a parcel', status_code=400)

    destination = user_input.get("destination")
    if not destination or destination.isspace():
        raise InvalidUsage('Destination is required', status_code=400)
    charset = re.compile('[A-Za-z]')
    checkmatch = charset.match(destination)
    if not checkmatch:
        raise InvalidUsage('Destination must be letters', status_code=400)

    pickup_location = user_input.get("pickup_location")
    if not pickup_location or pickup_location.isspace():
        raise InvalidUsage('Pickup location is required', status_code=400)
    charset = re.compile('[A-Za-z]')
    checkmatch = charset.match(pickup_location)
    if not checkmatch:
        raise InvalidUsage('Pickup location must be letters', status_code=400)

    parcel_id = len(parcels) + 1

    item_name = user_input.get("item_name")
    # if not item_name or item_name.isspace():
    #     raise InvalidUsage('Parcel item name is required', status_code=400)
    # charset = re.compile('[A-Za-z]')
    # checkmatch = charset.match(item_name)
    # if not checkmatch:
    #     raise InvalidUsage('Parcel item name must be letters', status_code=400)

    item_weight = user_input.get("item_weight")
    # if not item_weight:
    #     raise InvalidUsage('Parcel item weight is required', status_code=400)
    # if not isinstance(item_weight,int):
    #     raise InvalidUsage('Parcel item weight must be an integer', status_code=400)
    
    unit_delivery_price = user_input.get("unit_delivery_price")
    # if not item_weight:
    #     raise InvalidUsage('Parcel item unit delivery price is required', status_code=400)
    # if not isinstance(item_weight,int):
    #     raise InvalidUsage('Parcel item unit delivery price must be an integer', status_code=400)
    
    
    an_item = Items(item_name, item_weight, unit_delivery_price)
    the_item = an_item.create_item()
        
    parcel_object = Parcel(user_id, parcel_id, pickup_location, destination, items)
    parcel = parcel_object.create_a_parcel()
    if parcels:
        return parcel, 201
    else:
        raise InvalidUsage('Insertion failed', status_code=400)