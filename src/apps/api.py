from flask import Blueprint
from src.apps.v1 import apiV1

# Main api blueprint
apiBluePrint = Blueprint('APIs BluePrints', __name__, url_prefix="/api/")

# Register version 1 API blueprint
apiBluePrint.register_blueprint(apiV1)

