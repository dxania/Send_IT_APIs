from flask import Flask
from flask_jwt_extended import JWTManager
from app.controllers.db import DatabaseConnection

app = Flask(__name__)
db.setUp()

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'

jwt = JWTManager(app)

from app.routes import parcel_routes
from app.routes import user_routes
