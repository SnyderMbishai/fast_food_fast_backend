'''Order resource.'''
from flask import request
from flask_restful import Resource

from api.models import Meal, Order, User
from api.helpers.decorators import login_required, admin_required


class OrderResource(Resource):
    '''Class for handling orders.'''

    def get_role_and_user_id(self):
        '''Decode token and return data.'''
        authorization_header = request.headers.get('Authorization')
        access_token = authorization_header.split(' ')[1]
        payload = User.decode_token(access_token)
        return payload
