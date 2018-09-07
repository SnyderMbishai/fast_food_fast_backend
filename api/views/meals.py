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
