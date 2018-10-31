'''Create application.'''

from flask import Flask, render_template, Blueprint
from flask_restful import Api
from flask_cors import CORS

from main.config import configurations
# v1
from api.v1.views.welcome import WelcomeResource
from api.v1.views.user import UserResource
from api.v1.views.auth import AuthResource
from api.v1.views.meals import MealResource
from api.v1.views.orders import OrderResource, OrderManagement
from api.v1.views.manage_user import ManageUsersResource
# v2
from api.v2.views.user import DBUserResource
from api.v2.views.auth import DBAuthResource
from api.v2.views.meals import DBMealResource
from api.v2.views.orders import DBOrderResource
from api.v2.views.manage_user import DBManageUsersResource
from api.v2.views.orders import DBOrderManagement
from werkzeug.exceptions import BadRequest

def create_app(configuration):
    '''Create the flask app.'''

    app = Flask(__name__)
    CORS(app)
    api_blueprint = Blueprint('api', __name__)
    api = Api(api_blueprint)
    app.config.from_object(configurations[configuration])
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.url_map.strict_slashes = False
    app_context = app.app_context()
    app_context.push()
    # api = Api(app)

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

    # v2 urls
    api.add_resource(
        DBUserResource, '/api/v2/users/signup')
    api.add_resource(
        DBAuthResource, '/api/v2/users/signin')
    api.add_resource(
        DBMealResource, '/api/v2/meals', '/api/v2/meals/<int:meal_id>')
    api.add_resource(
        DBOrderResource, '/api/v2/orders/', '/api/v2/orders/<int:order_id>')
    api.add_resource(
        DBManageUsersResource, '/api/v2/users/manage/', '/api/v2/users/manage/<int:user_id>')
    api.add_resource(
        DBOrderManagement, '/api/v2/orders/accept/<int:order_id>')

    app.register_blueprint(api_blueprint)

    @app.route("/")
    def docs():
        '''Render the docstring'''
        return render_template("documentation.html")
    @api_blueprint.errorhandler(400)
    def handle_error(e):
        return {'dgfhgjh':'dfghjkl'}, 400

    return app
