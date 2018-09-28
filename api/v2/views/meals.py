'''Meals resource.'''

import re
from json import loads

from flask import request
from flask_restful import Resource, reqparse

from api.v2.models.meal_model import Meal
from api.v2.helpers.decorators import login_required, admin_required


class DBMealResource(Resource):
    '''Class for handling meals.'''

    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, type=str, help='Name (str) is required.')
    parser.add_argument('price', required=True, type=int, help='Price (int) is required.')

    @admin_required
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

    @login_required
    def get(self, meal_id=None):
        ''' Get meal/meals.'''

        # Get a single meal.
        if meal_id:
            meal = Meal.get(id=meal_id)
            if meal:
                meal=Meal(name=meal[1],price=meal[2])
                return {'message': 'Meal found.', 'meal': meal.view()}, 200
            return {'message': 'Meal not found.'}, 404

        # Get all meals
        meals = Meal.get_all()
        if not meals:
            return {'message': 'No meals found.'}, 404

        meals = [meal for meal in meals]
        for item in meals:
            item=Meal(name=item[1],price=item[2])
        return {'meals': meals}, 200

    @login_required
    @admin_required
    def put(self, meal_id):
        ''' Edit a meal.'''
        json_data = loads(request.data.decode())
        # import pdb; pdb.set_trace()
        name = json_data.get('name', None)
        price = json_data.get('price', None)
        new_data = {}



        meal = Meal.get(id=meal_id)

        if name:
            try:
                int(name)
                return {'message': "Invalid name!"}, 400
            except:
                if Meal.get(name=name):
                    return {'message': "A meal with that name exists!"}, 409
                elif isinstance(name, str):
                    new_data.update({'name': name})
                else:
                    return {'message': 'Name should be a string.'}, 400

        if price:
            if isinstance(price, int):
                new_data.update({'price': price})
            else:
                return {'message': 'Price should be an integer.'}, 400

        if meal:
            id=meal_id
            Meal.update(id=id, new_data=new_data)
            meal = Meal.get(id=id)
            mealn = Meal(name=meal[1],price=meal[2])
            meal = mealn.view(id)
            return {
                'message': 'Meal has been updated successfully.',
                'new_meal': meal}, 200
        return {'message': 'Meal does not exist.'}, 404

    @admin_required
    def delete(self, meal_id):
        '''Delete a meal.'''

        meal = Meal.get(id=meal_id)
        if meal:
            Meal.delete(meal_id)
            return{
                'message': 'Meal {} successfully deleted.'.format(meal_id)
            }, 200
        return {'message': 'Meal does not exist'}, 404
