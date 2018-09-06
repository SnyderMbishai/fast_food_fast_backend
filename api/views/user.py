'''User resource.'''

import re
from flask_restful import Resource, reqparse
from api.models import User

class UserResource(Resource):
    '''Class for handling user registration.'''

    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True, type=str, help='Username (str) is required.')
    parser.add_argument('email', required=True, type=str, help='Email (str) is required.')
    parser.add_argument('password', required=True, type=str, help='Password (str) is required.')

    def post(self):
        '''Create new user.'''
        
        arguments = UserResource.parser.parse_args()
        password = arguments.get('password')
        email = arguments.get('email')
        username = arguments.get('username')