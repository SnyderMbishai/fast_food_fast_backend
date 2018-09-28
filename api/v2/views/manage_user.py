import re
from flask import request
from flask_restful import Resource, reqparse
from api.v2.models.user_model import User
from api.v2.helpers.decorators import super_user_required


class DBManageUsersResource(Resource):
    '''Resource for managing users an admin.'''

    @super_user_required
    def put(self, user_id):
        '''Method for editing user roles to include admin'''

        user = User.get(id=user_id)
        if user:
            User.make_user_admin(user_id)
            return{'message': "User has been made admin successfully!"}, 200
        return{'message': "User was not found!"}, 404
