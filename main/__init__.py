"""Create application."""
from flask import Flask
from flask_restful import Api

from .config import configurations
from api.views.welcome import WelcomeResource


def create_app(configuration):
    """Create the flask app."""
    app = Flask(__name__)
    app.config.from_object(configurations[configuration])
    app_context = app.app_context()
    app_context.push()
    api = Api(app)
    api.add_resource(
        WelcomeResource, '/', '/api/v1')
    api.add_resource(
        UserResource, '/api/v1/users/signup',)
    api.add_resource(
        AuthResource, '/api/v1/users/signin')
    api.add_resource(
        MealResource, '/api/v1/meals', '/api/v1/meals/<int:meal_id>')
    api.add_resource(
        OrderResource, '/api/v1/orders/', '/api/v1/orders/<int:order_id>')
    api.add_resource(
        OrderManagement, '/api/v1/orders/accept/<int:order_id>')
    return app

app = create_app('testing')
