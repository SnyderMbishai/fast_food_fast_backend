"""Welcome resource."""
from flask_restful import Resource


class WelcomeResource(Resource):
    """Displays welcome message."""

    def get(self):
        """Display welcome message."""

        return {'message': 'Welcome to Fast Food Fast.'}, 200
