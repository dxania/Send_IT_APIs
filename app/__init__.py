from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
# import logging

app = Flask(__name__)

# CORS(app, allow_headers=[
#     "Content-Type", "Authorization", "Access-Control-Allow-Credentials", "Access-Control-Allow-Origin", "Access-Control-Allow-Headers"],
#     supports_credentials=True, intercept_exceptions=False)

CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})
# CORS(app, resources=r"/api/*")
# CORS(app)
# logging.getLogger('flask_cors').level = logging.DEBUG

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'

jwt = JWTManager(app)

from app.routes import parcel_routes
from app.routes import user_routes
