'''User resource.'''

import re
import json

from flask_restful import Resource, reqparse

from api.v1.models import User


class UserResource(Resource):
    '''Class for handling user registration.'''

    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True, type=str, help='Username (str) is required.')
    parser.add_argument('email', required=True, type=str, help='Email (str) is required.')
    parser.add_argument('password', required=True, type=str, help='Password (str) is required.')
    parser.add_argument('confirm_password', required=True, type=str, help='Password (str) is required.')

    def post(self):
        '''Create new user.'''

        arguments = UserResource.parser.parse_args()
        password = arguments.get('password')
        confirm_pwd = arguments.get('confirm_password')
        email = arguments.get('email')
        username = arguments.get('username')

        email_format = re.compile(r"([a-zA-Z0-9_.-]+@[a-zA-Z-]+\.[a-zA-Z-]+$)")
        username_format = re.compile(r"([a-zA-Z0-9]+$)")

        if not re.match(username_format, username):
            return {'message': 'Invalid username.'}, 400
        elif not re.match(email_format, email):
            return {
                'message': 'Invalid email.Example of a valid one:hero@gmail.com'
                }, 400
        elif password != confirm_pwd:
            return{'message':"passwords do not match!"}
        elif len(password)<8:
            return {'message': 'Invalid password. Password should be 8 or more characters long.'}, 400
        elif User.get_by_key(username=username):
            return {'message': 'Username already taken, if you are registered,please login to continue.'}, 400
        elif User.get_by_key(email=email):
            return {'message': 'Email already taken, if you are registered, please login to continue.'}, 400

        new_user = User(username=username, password=password, email=email)
        new_user.roles.append('user')
        new_user.save()
        token = new_user.generate_token()
        new_user = new_user.view()

        return {
            'message': 'User registration successful',
            'user': new_user,
            'token': token }, 201
