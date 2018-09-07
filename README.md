## Fast Food Fast.

[![Build Status](https://travis-ci.org/SnyderMbishai/fast_food_fast_backend.svg?branch=develop_v1)](https://travis-ci.org/SnyderMbishai/fast_food_fast_backend)
[![Coverage Status](https://coveralls.io/repos/github/SnyderMbishai/fast_food_fast_backend/badge.svg?branch=ft-add-helpers-160346910)](https://coveralls.io/github/SnyderMbishai/fast_food_fast_backend?branch=ft-add-helpers-160346910)
[![Maintainability](https://api.codeclimate.com/v1/badges/c58e13d5bd032ed9dba9/maintainability)](https://codeclimate.com/github/SnyderMbishai/fast_food_fast_backend/maintainability)

### Link to heroku

https://f-f-f-v1.herokuapp.com/

### Prerequisites

1. Python 3: https://www.python.org/downloads/
2. Flask: http://flask.pocoo.org/docs/1.0/installation/
3. Flask_restful: https://flask-restful.readthedocs.io/en/latest/installation.html
4. Pytest: https://docs.pytest.org/en/latest/getting-started.html

### Endpoints

| Endpoint                             | Method   | Description                         |
| ------------------------------------ | -------- | ----------------------------------- |
| /api/v1/users/signup                 | POST     | signup a user                       |
| /api/v1/users/signin                 | POST     | signin a user                       |
| /api/v1/meals                        | POST     | create a meal                       |
| /api/v1/meals/<int:meal_id>          | GET/PUT  | get/edit a specific meal            |
| /api/v1/orders/                      | POST/GET | creat order,get all orders          |
| /api/v1/orders/<int:order_id>        | PUT/GET  | edit an order, get a specific order |
| /api/v1/orders/accept/<int:order_id> | PATCH    | complete, accept, reject order      |

### Running and testing app

    $ virtualenv venv
    $ cd venv
    $ git clone https://github.com/SnyderMbishai/fast_food_fast_backend.git
    $ source venv/bin/activate
    $ cd fast_food_fast_backend
    $ export APP_SETTINGS=development
    $ export APP_SECRET_KEY="sdfghjklsdfghj"
    $ python run.py

##### Testing

follow the steps above then :

$ python -m pytest

### Author

Snyder Mbishai

### Contributions

This repo can be forked and contributed to.
