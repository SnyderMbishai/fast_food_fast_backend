'''Order resource.'''
from flask import request
from flask_restful import Resource

from api.v2.models.meal_model import Meal
from api.v2.models.order_model import Order
from api.v2.models.user_model import User
from api.v2.helpers.decorators import login_required, admin_required


class DBOrderResource(Resource):
    '''Class for handling orders.'''

    @login_required
    def post(self):
        '''Create an order.'''

        data = request.get_json(force=True)
        user_id = data.get('user_id', None)
        meal_dict = data.get('meal_dict', None)

        if not isinstance(user_id, int):
            return {'message': 'user_id (int) is required.'}, 400
        if not isinstance(meal_dict, dict):
            return {'message': 'meal_dict (dict) is required.'}, 400

        # Check if meal ordered exist.
        meal_ids = meal_dict.keys()
        for meal_id in meal_ids:
            try:
                meal_id = int(meal_id)
                meal = Meal.get(id=int(meal_id))
                if meal:
                    if not isinstance(meal_dict[str(meal_id)], int):
                        return {
                            'message': 'Meal quantities should be integers.'
                        }, 400
                else:
                    return {
                        'message': 'Meal {} does not exist.'.format(meal_id)
                    }, 400
            except ValueError:
                return {'message': 'Meal ID should be an integer.'}, 400

        order = Order(user_id=user_id, meal_dict=meal_dict)
        order_id = order.add_order()

        return {
            'message': 'Order has been created successfully.',
            'order_id': order_id,
            'meals': Order.get_meals(order_id)
        }, 201

    @login_required
    def get(self, order_id=None):
        '''Get order.'''
        authorization_header = request.headers.get('Authorization')
        access_token = authorization_header.split(' ')[1]
        payload = User.decode_token(token=access_token)
        roles, user_id = payload['roles'], payload['user_id']
        is_admin = 'admin' in roles
        if order_id:
          order = Order.get(id=order_id)
          if order is None:
            return {'message': 'Order not found.'}, 404
          print('>>>>',order[1], user_id, is_admin)
          if order[1] == user_id or is_admin:
            return {'message': 'Order found.', 'order': Order.view(order)}, 200
          else:
            return {
                'message': 'You do not have permission to see this order.'
            }, 403
        else:
          # import pdb; pdb.set_trace()
          if is_admin:
            orders = Order.get_all()
          else:
            orders = Order.get(user_id=user_id)
            print('all mine', orders)
            if len(orders) == 0:
              return {'message': 'Orders not found'}, 404
            orders = [Order.view(order) for order in orders]
            return {'message': 'Orders found.', 'orders': orders}, 200


    @login_required
    def put(self, order_id):
        '''Edit order details.'''

        data = request.get_json(force=True)
        new_data = data.get('new_data')
        payload = self.get_role_and_user_id()
        user_id = payload['user_id']

        order_id = int(order_id)
        order = Order.get(id=order_id)
        if not order:
            return {'message': 'Order does not exist.'}, 404
        print(order.user, user_id)
        if order.user['id'] == user_id:
            new_data.update({'user_id': user_id})
            new_order = order.update(new_data=new_data)
            return {
                'message': 'Order updated successfully.', 'new_order': new_order
            }, 200
        return {
            'message': 'You do not have permission to edit this order.'
        }, 403

    @login_required
    @admin_required
    def delete(self, order_id):
        '''Method for deleting an order.'''

        order = Order.get_by_key(id=order_id)
        if not order:
            return {'message': 'Order does not exist'}, 404
        order.delete()
        return{
            'message': 'Successfully deleted Order {}.'.format(order_id)
        }, 200

    @login_required
    @admin_required
    def patch(self, order_id):
        '''Mark order as completed.'''

        order = Order.get(id=order_id)
        if not order:
            return {'message': 'Order does not exist.'}, 404
        order.completed = True
        order.save()
        return {
            'message': 'Order {} has been completed.'.format(order_id)}, 200


class DBOrderManagement(Resource):
    '''Manage orders.'''

    @login_required
    @admin_required
    def patch(self, order_id):
        '''Accept or decline order.'''

        data = request.get_json(force=True)
        accepted = data.get('accepted')
        # Ensure accepted is a boolean.
        if not isinstance(accepted, bool):
            return {'message': 'accept should be a boolean.'}, 400
        order = Order.get(id=order_id)
        # if order is not found
        if not order:
            return {'message': 'Order does not exist.'}, 404
        if not order.completed:
            # if accepted = True
            if accepted:
                order.accepted = accepted
                order.save()
                return {
                    'message': 'Order {} has been accepted.'.format(order_id)
                }, 200
            # decline order
            order.accepted = accepted
            return {
                'message': 'Order {} has been declined.'.format(order_id)}, 200
        # you cannot accept/decline an already completed order
        return {'message': 'This order has already been completed.'}, 200
