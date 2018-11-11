from flask import Flask

app = Flask(__name__)

from app.routes import parcel_routes
from app.routes import user_routes
