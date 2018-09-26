"""Welcome resource."""
from flask_restful import Resource
from flask import render_template


class WelcomeResource(Resource):
    """Displays welcome message."""

    def get(self):
        """Display welcome message."""
        # return {'message': 'Welcome to Fast Food Fast.'}, 200
        return render_template("documentation.html")
