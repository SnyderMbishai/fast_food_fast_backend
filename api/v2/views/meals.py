'''Meals resource.'''

import re
from json import JSONDecodeError

from flask import request
from flask_restful import Resource, reqparse

from api.v2.models.meal_model import Meal
from api.helpers.decorators import login_required, admin_required


class DBMealResource(Resource):
    '''Class for handling meals.'''

    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, type=str, help='Name (str) is required.')
    parser.add_argument('price', required=True, type=int, help='Price (int) is required.')

    def post(self):
        '''Create a new meal.'''
        # print(request.get_json())
        arguments = DBMealResource.parser.parse_args()
        name = arguments.get('name')
        price = arguments.get('price')
        name_format = re.compile(r"([a-zA-Z0-9])")
        

        if not re.match(name_format, name):
            return{'message': "Invalid name!"},400

        meal_exists = Meal.get(name=name)
        if meal_exists:
            return {'message': 'Meal with that name already exists.'},409
        meal = Meal(name=name, price=price)
        meal.add_meal()
        meal = meal.view()

        return {'message': 'Meal successfully added.', 'meal': meal}, 201
