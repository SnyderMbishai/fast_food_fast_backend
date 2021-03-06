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
        meal_dict1 = data.get('meal_dict')

        authorization_header = request.headers.get('Authorization')
        access_token = authorization_header.split(' ')[1]
        payload = User.decode_token(token=access_token)
        user_id = payload['user_id']

        if not isinstance(user_id, int):
            return {'message': 'user_id (int) is required.'}, 400
        if not isinstance(meal_dict1, dict):
            return {'message': 'meal_dict (dict) is required.'}, 400
        if meal_dict1 is None:
            return{'message': "You haven't selected any meals"}, 200

        # Check if meal ordered exist.
        meal_ids = meal_dict1.keys()
        meals_not_found = []
        meals_found = {}

        for meal_id in meal_ids:
            try:
                meal_id = int(meal_id)
                meal = Meal.get(id=int(meal_id))
                if meal:
                    if not isinstance(int(meal_dict1[str(meal_id)]), int):
                        return {
                            'message': 'Meal quantities should be integers.'
                        }, 400
                    meals_found.update({meal_id: meal_dict1[str(meal_id)]})
                else:
                    meals_not_found.append(meal_id)

            except Exception:
                return {'message': 'Meal ID should be an integer.'}, 400
        if not meal_dict1:
            return {
                'message': 'Meal IDs provided are invalid.',
                'meal_ids_not_found': meals_not_found
            }, 404
        order = Order(user_id=user_id, meal_dict=meals_found)

        order_id = order.add_order()
        return {
            'message': 'Order has been created successfully.',
            'order_id': order_id,
            'meals': Order.get_meals(order_id),
            'meal_ids_not_found': meals_not_found
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
            if order[1] == user_id or is_admin:
                return {'message': 'Order found.', 'order': Order.view(order)}, 200
            else:
                return {
                    'message': 'You do not have permission to see this order.'
                }, 403
        else:
            if is_admin:
                orders = Order.get_all()
                orders = [Order.view(order) for order in orders]
                return {'message': "Orders found.", 'orders': orders}, 200
            else:
                orders = Order.get_all_by_user_id(user_id=user_id)
                if len(orders) == 0:
                    return {'message': 'Orders not found'}, 404
                orders = [Order.view(order) for order in orders]
                return {'message': 'Orders found.', 'orders': orders}, 200

    @login_required
    def put(self, order_id):
        '''Edit order details.'''
        data = request.get_json(force=True)
        new_data = data.get('new_data')
        # get user_id
        authorization_header = request.headers.get('Authorization')
        access_token = authorization_header.split(' ')[1]
        payload = User.decode_token(token=access_token)
        user_id = payload['user_id']
        order = Order.get(id=order_id)
        if not order:
            return {'message': 'Order does not exist.'}, 404
        print(order[1], user_id)
        if order[1] == user_id:
            new_info = []
            for key, val in new_data['meals_dict'].items():
                new_info.append({'meal_id': key, 'quantity': val})
            new_order = Order.update(int(order_id), new_info)
            new_order = Order.view(new_order)
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
        order = Order.get(id=order_id)
        if not order:
            return {'message': 'Order does not exist'}, 404
        Order.delete(order_id)
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
        Order.complete_order(order_id)
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
        if order[2] is False:
            # accept order
            if accepted is True:
                Order.accept_order(order_id, status=True)
                return {
                    'message': 'Order {} has been accepted.'.format(order_id)
                }, 200
            # decline order
            Order.accept_order(order_id, status=False)
            return {
                'message': 'Order {} has been declined.'.format(order_id)}, 200
        # you cannot accept/decline an already completed order
        return {'message': 'This order has already been completed.'}, 200
