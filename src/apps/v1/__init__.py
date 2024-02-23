from flask import Blueprint
from src.apps.v1.UserView import userApi

apiV1 = Blueprint('API version 1 BluePrints', __name__, url_prefix="v1/")

# Register version 1 API blueprints
apiV1.register_blueprint(userApi)
