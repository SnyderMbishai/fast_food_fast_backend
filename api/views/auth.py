"""User resource."""
import re
from flask_restful import Resource, reqparse
from api.models import User


class AuthResource(Resource):
    """Register new user."""

    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True, type=str, help='Username (str) is required.')
    parser.add_argument('password', required=True, type=str, help='Password (str) is required.')
    
    def post(self): 
        """Resource for managing user authentication."""
        
        arguments = AuthResource.parser.parse_args()
        password = arguments.get('password')
        username = arguments.get('username')
        user = User.get_by_key(username=username)
        if not user or not user.check_password(password=password):
            return {'message': 'Username/Password Invalid.'}, 401
        token = user.generate_token()

        return {'message': 'User login successful.', 'token': token }, 200