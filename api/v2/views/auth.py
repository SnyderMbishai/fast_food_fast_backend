"""User resource."""
import re
from flask import request
from flask_restful import Resource, reqparse
from api.v2.models.user_model import User


class DBAuthResource(Resource):
    """Login a user."""

    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True, type=str, help='Username (str) is required.')
    parser.add_argument('password', required=True, type=str, help='Password (str) is required.')
    
    def post(self): 
        """Resource for managing user authentication."""
        
        arguments = DBAuthResource.parser.parse_args()
        password = arguments.get('password')
        username = arguments.get('username')
        user = User.get(username=username)
        user = User(username=username,email=user[2],password=user[3])
        print(user)

        if user:                
            if  not user.check_password(username,password):
                return {'message': 'Wrong password.'}, 401
            token = user.generate_token()
            return {'message': 'User login successful.', 'token': token }, 200
        return{'message':"Username not registered. Correct it or register first."},401