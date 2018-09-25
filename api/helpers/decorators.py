'''Decorators to implement authorization.'''

from functools import wraps
from flask import request
from api.models import User


def login_required(func):
    '''Check if user has a valid token.'''
    @wraps(func)
    def decorated(*args, **kwargs):
        authorization_header = request.headers.get('Authorization')
        if authorization_header:
            access_token = authorization_header.split(' ')[1]
            roles = User.decode_token(token=access_token)['roles']
            if ('user' in roles):
                return func(*args, **kwargs)
        return {'message': 'Ensure you have an authorization header.'}, 400
    return decorated


def admin_required(func):
    '''Check if user has a valid admin token.'''

    @wraps(func)
    def decorated(*args, **kwargs):
        authorization_header = request.headers.get('Authorization')
        if authorization_header:
            access_token = authorization_header.split(' ')[1]
            roles = User.decode_token(token=access_token)['roles']
            if ('admin' in roles):
                return func(*args, **kwargs)
            return {'message': 'This action requires an admin token.'}, 403
        return{'message':'Ensure you have an authorization header.'}
    return decorated

def super_user_required(func):
    '''Check whether user is a super admin'''
    @wraps(func)

    def decorated(*args, **kwargs):
        authorization_header = request.headers.get('Authorization')
        if authorization_header:
            access_token = authorization_header.split(' ')[1]
            roles = User.decode_token(token=access_token)['roles']
            if 'superuser' in roles:
                return func(*args, **kwargs)
            return {'message': 'This action requires a superuser token.'}, 403
        return{'message':'Ensure you have an authorization header.'}                                
    return decorated