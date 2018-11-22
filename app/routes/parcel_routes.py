from app import app
from app.controllers.parcel_controller import Parcel_Controller
from flask import request, jsonify
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)


@app.route('/')
def index():
    """Index page"""
    return Parcel_Controller.index()

@app.route('/api/v1/parcels', methods = ['GET'])
@jwt_required
def parcels():
    """Retrieve all parcels"""
    return Parcel_Controller.get_parcels()

@app.route('/api/v1/users/<user_id>/parcels', methods = ['GET'])
@jwt_required
def get_parcels_by_user(user_id):
    """Retrieve all parcels by a specific user"""
    return Parcel_Controller.get_parcels_by_user(user_id)

@app.route('/api/v1/parcels/<int:parcel_id>', methods = ['GET'])
@jwt_required
def get_parcel(parcel_id):
    """Retrieve a particular parcel"""
    return Parcel_Controller.get_parcel(parcel_id)


@app.route('/api/v1/parcels/<int:parcel_id>/present_location', methods = ['PUT'])
@jwt_required
def change_location(parcel_id):
    """Change the present location of a parcel delivery order"""
    return Parcel_Controller.change_present_location(parcel_id)


@app.route('/api/v1/parcels/<int:parcel_id>/status', methods = ['PUT'])
@jwt_required
def change_status(parcel_id):
    """Cancel a particular parcel delivery order by a user"""
    return Parcel_Controller.change_parcel_status(parcel_id)


@app.route('/api/v1/parcels/<int:parcel_id>/destination', methods = ['PUT'])
@jwt_required
def change_destination(parcel_id):
    return Parcel_Controller.change_parcel_destination(parcel_id)


@app.route('/api/v1/parcels', methods =['POST'])
@jwt_required
def create_parcel():
    """Create a parcel function wrapped around the Post /parcels endpoint"""
    return Parcel_Controller.create_parcel()
