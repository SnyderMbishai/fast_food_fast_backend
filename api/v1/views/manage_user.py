"""User management resource."""

from flask_restful import Resource

from api.v1.models import User
from api.helpers.decorators import super_user_required


class ManageUsersResource(Resource):
    '''Resource for managing users an admin.'''

    @super_user_required
    def put(self, user_id):
        '''Method for editing user roles to include admin'''
        user = User.get(id=user_id)
        if user:
            User.make_user_admin(user)
            return{'message': "User has been made admin successfully!"}, 200
        return{'message': "User was not found!"}, 404
