import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} 
    where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks = Drink.query.all()
    drinks = [drink.short_rep() for drink in drinks]
    return jsonify({"success": True, "drinks": drinks})


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} 
    where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth(permission='drink detail')
def get_drink():
    # drink = Drink.query.filter_by(id=drink_id).first()
    # if not drink:
        # abort(404)
    drinks = Drink.query.all()
    drink = [drink.long_rep() for drink in drinks]
    return jsonify({"success": True, "drinks": drink})


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} 
    where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth(permission='add drink')
def add_drink():
    data = request.get_json()
    title = data.get('title')
    recipe = data.get('recipe')
    if not isinstance(recipe, list):
        return jsonify({"success": False,
                        "error": 
                            "Recipe field must contain a list of recipe objects e.g [{'color': 'blue'}]"}), 400
    drink = Drink(title=title, recipe=recipe)
    check_drink = Drink.query.filter_by(title=drink.title).first()
    if check_drink:
        return jsonify({"success": False,
                        "error": f"Drink with title {drink.title} already exists"}), 400
    drink.insert()
    return jsonify({"success": True, "drink": drink.long_rep()}), 201


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} 
    where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<drink_id>', methods=["PATCH"])
@requires_auth(permission='edit drink')
def update_drink(drink_id):
    data = request.get_json()
    title = data.get("title")
    recipe = data.get("recipe")
    drink = Drink.query.filter_by(id=drink_id).first()
    if not drink:
        abort(404)
    print(title)
    if title:
        setattr(drink, "title", title)
        drink.update()
    if recipe:
        setattr(drink, "recipe", recipe)
        drink.update()
    return jsonify({"success": True,
                    "drink": drink.long_rep()
                    }), 200
    


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} 
    where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<drink_id>', methods=['DELETE'])
@requires_auth(permission='delete drink')
def delete_drink(drink_id):
    drink =  Drink.query.filter_by(id=drink_id).first()
    if not drink:
        abort(404)
    drink.delete()
    return jsonify({"success": True, "delete": drink.id}), 200


## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''
@app.errorhandler(404)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(500)
def autherror(error):
    if isinstance(error, AuthError):
        return jsonify({"success": False,
                    "error": error.status_code,
                    "message": error.error}), error.status_code
