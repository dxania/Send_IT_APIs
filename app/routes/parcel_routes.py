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
    return Parcel_Controller.cancel_parcel(parcel_id)


@app.route('/api/v1/users/<int:user_id>/<int:parcel_id>/cancel', methods = ['PUT'])
def cancel_parcel_by_user(parcel_id, user_id):
    """Cancel a particular parcel delivery order by a user"""
    return Parcel_Controller.cancel_parcel_by_user(parcel_id, user_id)

   
@app.route('/api/v1/parcels', methods =['POST'])
def create_parcel():
    """Create a parcel function wrapped around the Post /parcels endpoint"""
    return Parcel_Controller.create_parcel()