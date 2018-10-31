'''User management resource.'''

from flask_restful import Resource

from api.v2.models.user_model import User, UserRoles
from api.v2.helpers.decorators import super_user_required


class DBManageUsersResource(Resource):
    '''Resource for managing users an admin.'''

    @super_user_required
    def put(self, user_id):
        '''Method for editing user roles to include admin'''
        user = User.get(id=user_id)
        if user:
            # check if a user i already an admin
            user_roles = UserRoles.get_user_roles(user[0])
            if 'admin' not in user_roles:
                User.make_user_admin(user_id)
                return{'message': "User has been made admin successfully!"}, 200
            return{"message": "User {} is already an admin.".format(user_id)}
        return{'message': "User was not found!"}, 404

    @super_user_required
    def get(self, id=None):
        if id:
            user = User.get(id=id)
            if user:
                return{"message": "User found.", "user": user.view()}, 200
            return{"message": "User not found."}, 404

        users = User.get_all()
        if users:
            print([User.view_details(user)for user in users])
            print(">>>>>>>>>>")
            users = [User.view_details(user) for user in users]
            return{"message": "Users found.", "users": users}, 200
        return{"Users not found."}, 404
