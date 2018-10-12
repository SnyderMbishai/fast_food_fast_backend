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
        WelcomeResource,
        '/',
        '/api/v1/',
        '/api/v1'
    )
    return app

app = create_app('testing')
