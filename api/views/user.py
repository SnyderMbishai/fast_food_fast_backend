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

        email_format = re.compile(r"([a-zA-Z0-9_.-]+@[a-zA-Z-]+\.[a-zA-Z-]+$)")
        username_format = re.compile(r"([a-zA-Z0-9]+$)")

        if not re.match(username_format, username):
            return {'message': 'Invalid username.'}, 400
        elif not re.match(email_format, email):
            return {'message': 'Invalid email.'}, 400
        elif len(password)<8:
            return {'message': 'Invalid password. Password should be 8 or more characters long.'}, 400
        elif User.get_by_key(username=username) or User.get_by_key(email=email):
            return {'message': 'Username/Email not available.'}, 400
