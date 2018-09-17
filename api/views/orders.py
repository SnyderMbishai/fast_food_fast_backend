'''Order resource.'''
from flask import request
from flask_restful import Resource

from api.models import Meal, Order, User
from api.helpers.decorators import login_required, admin_required


class OrderResource(Resource):
    '''Class for handling orders.'''

    @login_required
    def get_role_and_user_id(self):
        '''Decode token and return data.'''

        authorization_header = request.headers.get('Authorization')
        access_token = authorization_header.split(' ')[1]
        payload = User.decode_token(access_token)
        return payload

    @login_required
    def post(self):
        '''Create an order.'''

        data = request.get_json(force=True)
        user_id = data.get('user_id')
        meal_dict = data.get('meal_dict')

        if not isinstance(user_id, int):
            return {'message': 'user_id (int) is required.'}, 400
        if not isinstance(meal_dict, dict):
            return {'message': 'meal_dict (dict) is required.'}, 400

        # Check if meal ordered exist.
        meal_ids = meal_dict.keys()
        for meal_id in meal_ids:
            try:
                meal_id = int(meal_id)
                meal = Meal.get_by_key(id=int(meal_id))
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
        order = Order(user_id=user_id, meals_dict=meal_dict)
        order = order.save()
        return {
            'message': 'Order has been created successfully.', 'order': order
        }, 201
    @login_required
    def get(self, order_id=None):
        '''Get order.'''

        payload = self.get_role_and_user_id()
        roles, user_id = payload['roles'], payload['user_id']

        is_admin = True if ('admin' in roles) else False
        if order_id:
            order = Order.get(id=order_id)
            if order:
                if order.user['id'] == user_id or is_admin:
                    return {
                        'message': 'Order found.', 'order': order.view()
                    }, 200
                return {
                    'message': 'You do not have permission to see this order.'
                }, 403
            return {'message': 'Order not found.'}, 404
        if is_admin:
            orders = Order.get_all()
            orders = [orders[order].view() for order in orders]
            return {'message': 'Orders found.', 'orders': orders}, 200
        user = User.get(id=user_id).view()
        orders = Order.get_many_by_key(user=user)
        orders = [order.view() for order in orders]
        return {'message': 'Orders found.', 'orders': orders}, 200
    @login_required
    def put(self, order_id):
        '''Edit order details.'''

        data = request.get_json(force=True)
        new_data = data.get('new_data')
        print(new_data)
        payload = self.get_role_and_user_id()
        user_id = payload['user_id']

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
        order = Order.get(order_id)
        if order:
            order.delete()
            return{
                'message': 'Order {} successfully deleted.'.format(order_id)
            }, 200
        return {'message': 'Order does not exist'}, 404



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

class OrderManagement(Resource):
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
        return {'message': 'This order has already been completed.'}, 202
