import re

from flask import jsonify, flash, request, make_response

from app.exception_handler import InvalidUsage

from app import app

from app.models.parcel_models import Parcel, parcels, Items



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
    all_parcels = parcel.get_all_parcels()
    if all_parcels:
        return all_parcels, 200
    else:
        raise InvalidUsage('There are no parcels in the store', status_code=204) 
    

@app.route('/api/v1/parcels/<int:parcel_id>', methods = ['GET'])
def get_parcel(parcel_id):
    """Retrieve a particular parcel 
    function wrapped around the Get 
    /parcel/<int:parcel_id> endpoint
    """
    a_single_parcel = parcel.get_a_parcel(parcel_id)
    if a_single_parcel:
        return a_single_parcel, 200
    else:
        raise InvalidUsage('There is no parcel matching that ID', status_code=204)

@app.route('/api/v1/parcels/<int:user_id>/<int:parcel_id>/cancel', methods = ['PUT'])
def cancel_parcel(parcel_id, user_id):
    """Cancel a particular parcel delivery order
    function wrapped around the Put
    /parcels/<int:user_id>/<int:parcel_id> endpoint
    """
    for user in users:
        if not user_id:
            raise InvalidUsage('You dont have rights to cancel this parcel delivery order', status_code=400)
        else:
            a_single_parcel = parcel.cancel_parcel_delivery_order(parcel_id, user_id)
            return a_single_parcel, 202

   
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
    #if not isinstance(items, list):
        # raise InvalidUsage('Items must be a list', status_code=400)


    # total_weight = Items.get_total_weight(items)
    # no_of_items = len(items)

    user_id = user_input.get("user_id")
    #for user in users:
        #if not user_id:
            #raise InvalidUsage('That user id does not exist, you cannot create a parcel', status_code=400)

    destination = user_input.get("destination")
    # if not destination or destination.isspace():
    #     raise InvalidUsage('destination is required', status_code=400)
    # charset = re.compile('[A-Za-z]')
    # checkmatch = charset.match(destination)
    # if not checkmatch:
    #     raise InvalidUsage('destination must be letters', status_code=400)

    pickup_location = user_input.get("pickup_location")
    # if not pickup_location or pickup_location.isspace():
    #     raise InvalidUsage('pickup_location is required', status_code=400)
    # charset = re.compile('[A-Za-z]')
    # checkmatch = charset.match(pickup_location)
    # if not checkmatch:
    #     raise InvalidUsage('pickup_location must be letters', status_code=400)

    parcel_id = len(parcels) + 1
        
    parcel_object = Parcel(user_id, parcel_id, pickup_location, destination, items)
    parcel = parcel_object.create_a_parcel()
    if parcels:
        return parcel, 201
    else:
raise InvalidUsage('Insertion failed', status_code=400)