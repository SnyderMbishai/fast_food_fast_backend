'''User resource.'''

import re

from flask import request
from flask_restful import Resource, reqparse

from api.models import Meal


class MealResource(Resource):
    '''Class for handling meals.'''

    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, type=str, help='Name (str) is required.')
    parser.add_argument('price', required=True, type=int, help='Price (int) is required.')