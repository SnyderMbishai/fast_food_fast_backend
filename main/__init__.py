'''Create application.'''

from flask import Flask, render_template
from flask_restful import Api

from main.config import configurations
from api.v1.views.welcome import WelcomeResource
from api.v1.views.user import UserResource
from api.v1.views.auth import AuthResource
from api.v1.views.meals import MealResource
from api.v1.views.orders import OrderResource, OrderManagement
from api.v1.views.manage_user import ManageUsersResource


def create_app(configuration):
    '''Create the flask app.'''
    
    app = Flask(__name__)
    app.config.from_object(configurations[configuration])
    app.url_map.strict_slashes = False
    app_context = app.app_context()
    app_context.push()
    api = Api(app)
    # api.add_resource(
    #     WelcomeResource, '/', '/api/v1')
    api.add_resource(
        UserResource, '/api/v1/users/signup')
    api.add_resource(
        AuthResource, '/api/v1/users/signin')
    api.add_resource(
        MealResource, '/api/v1/meals', '/api/v1/meals/<int:meal_id>')
    api.add_resource(
        OrderResource, '/api/v1/orders/', '/api/v1/orders/<int:order_id>')
    api.add_resource(
        OrderManagement, '/api/v1/orders/accept/<int:order_id>')
    api.add_resource(
        ManageUsersResource, '/api/v1/users/manage/<int:user_id>')
    
    @app.route("/")
    def docs():
        return render_template("documentation.html")
    
    return app
