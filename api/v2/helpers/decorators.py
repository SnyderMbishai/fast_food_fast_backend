'''Decorators to implement authorization.'''

from functools import wraps
from flask import request
from api.v2.models.user_model import User


def get_access_token(authorization_header):
    '''Get a user's access from the authorization header.'''
    bearer_token = authorization_header.split(' ')
    return bearer_token[-1]

def login_required(func):
    '''Check if user has a valid token.'''
    @wraps(func)
    def decorated(*args, **kwargs):
        '''Check if user is logged in by decoding the token.'''
        authorization_header = request.headers.get('Authorization')
        if authorization_header:
            access_token = get_access_token(authorization_header)
            roles = User.decode_token(token=access_token)['roles']
            if 'user' in roles:
                return func(*args, **kwargs)
            return {'message': 'You do not have requied permission.'}, 400
        return {'message': 'Ensure you have an authorization header.'}, 400
    return decorated

def admin_required(func):
    '''Check if user has a valid admin token.'''
    @wraps(func)
    def decorated(*args, **kwargs):
        '''Check if user is an admin by decoding the token.'''
        authorization_header = request.headers.get('Authorization')
        if authorization_header:
            access_token = get_access_token(authorization_header)
            roles = User.decode_token(token=access_token)['roles']
            if 'admin' in roles:
                return func(*args, **kwargs)
            return {'message': 'This action requires an admin token.'}, 403
        return{'message': 'Ensure you have an authorization header.'}, 400
    return decorated

def super_user_required(func):
    '''Check whether user is a super admin'''
    @wraps(func)
    def decorated(*args, **kwargs):
        '''Check if user is a superuser by decoding the token.'''
        authorization_header = request.headers.get('Authorization')
        if authorization_header:
            access_token = get_access_token(authorization_header)
            roles = User.decode_token(token=access_token)['roles']
            if 'superuser' in roles:
                return func(*args, **kwargs)
            return {'message': 'This action requires a superuser token.'}, 403
        return{'message': 'Ensure you have an authorization header.'}
    return decorated
