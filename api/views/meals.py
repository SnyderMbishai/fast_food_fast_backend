'''Meals resource.'''

import re

from flask import request
from flask_restful import Resource, reqparse

from api.models import Meal


class MealResource(Resource):
    '''Class for handling meals.'''

    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, type=str, help='Name (str) is required.')
    parser.add_argument('price', required=True, type=int, help='Price (int) is required.')

    def post(self):
        '''Create a new meal.'''
        
        arguments = MealResource.parser.parse_args()
        name = arguments.get('name')
        price = arguments.get('price')

        meal_exists = Meal.get_by_key(name=name)
        if meal_exists:
            return {'message': 'Meal with that name already exists.'}, 202
        meal = Meal(name=name, price=price)
        meal = meal.save()

        return {'message': 'Meal successfully added.', 'meal': meal}, 201

    def get(self, meal_id=None):
        ''' Get meal/meals.'''
        
        # Get a single meal.
        if meal_id:
            meal = Meal.get_by_key(id=meal_id)
            if meal:
                return {'message': 'Meal found.', 'meal': meal.view()}, 200
            return {'message': 'Meal not found.'}, 404

        # Get all meals
        meals = Meal.get_all()
        if not meals:
            return {'message': 'No meals found.'}, 404
        meals = [meals[key].view() for key in meals]
        return {'meals': meals}, 200

    def put(self, meal_id):
        ''' Edit a meal.'''

        json_data = request.get_json()
        name = json_data.get('name', None)
        price = json_data.get('price', None)
        new_data = {}
        if name:
            if isinstance(name, str):
                new_data.update({'name': name})
            else:
                return {'message': 'Name should be a string.'}, 400
        if price:
            if isinstance(price, int):
                new_data.update({'price': price})
            else:
                return {'message': 'Price should be an integer.'}
        meal = Meal.get_by_key(meal_id=meal_id)
        if meal:
            meal = meal.update(new_data=new_data)
            return {
                'message': 'Meal has been updated successfully',
                'new_meal': meal}, 200
        return {'message': 'Meal does not exist'}, 404

    def delete(self, meal_id):
        '''Delete a meal.'''
        
        meal = Meal.get(meal_id)
        if meal:
            meal.delete()
            return{
                'message': 'Meal {} successfully deleted.'.format(meal_id)
            }, 200
        return {'message': 'Meal does not exist'}, 404
