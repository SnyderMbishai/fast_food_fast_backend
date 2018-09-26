"""User resource."""
import re
from flask import request
from flask_restful import Resource, reqparse
from api.v1.models import User


class AuthResource(Resource):
    """Login a user."""

    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True, type=str, help='Username (str) is required.')
    parser.add_argument('password', required=True, type=str, help='Password (str) is required.')
    
    def post(self): 
        """Resource for managing user authentication."""
        
        arguments = AuthResource.parser.parse_args()
        password = arguments.get('password')
        username = arguments.get('username')
        user = User.get_by_key(username=username)

        # if request.headers.get('content_type') !=  'application/json':
        #     return{'message':"Make sure content_type is application/json"}
        if user:                
            if  not user.check_password(password=password):
                return {'message': 'Wrong password.'}, 401
            token = user.generate_token()
            return {'message': 'User login successful.', 'token': token }, 200
        return{'message':"Username not registered. Correct it or register first."},401