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
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
def get_drinks():
   drinks = Drink.query.all()
   drink_details = [drink.short() for drink in drinks]
   return (
                jsonify(
                    {
                        "success": True,
                        "drinks": drink_details,
                    }
                ),
                200,
            )


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drink_detail(jwt):
   drinks = Drink.query.all()
   drink_details = [drink.long() for drink in drinks]
   return (
                jsonify(
                    {
                        "success": True,
                        "drinks": drink_details,
                    }
                ),
                200,
            )

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods = ['POST'])
@requires_auth('post:drinks')
def post_drinks(jwt):
  
    data = request.json
  
    title = data["title"]
    recipe = data["recipe"]
   
    drink_recipe = []
    app.logger.info("recipe")
    app.logger.info(recipe)

    if type(recipe) is dict:
        ingredient_name = recipe['name']
        ingredient_color = recipe['color']
        ingredient_parts = recipe['parts']
        drink_recipe.append({
                'name': ingredient_name,
                'color': ingredient_color,
                'parts': ingredient_parts
            })
    else:
        for ingredient in recipe:
            ingredient_name = ingredient['name']
            ingredient_color = ingredient['color']
            ingredient_parts = ingredient['parts']
            drink_recipe.append({
                'name': ingredient_name,
                'color': ingredient_color,
                'parts': ingredient_parts
            })

    json_drink_recipe = json.dumps(drink_recipe)

    drink = Drink(title=title, recipe=json_drink_recipe)
    app.logger.info(json_drink_recipe)
#    new_drink = Drink(title, recipe)
    drink.insert()

    return (
                jsonify(
                    {
                        "success": True,
                        "drinks": [drink.long()]
                    }
                ),
                200,
            )

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods = ['PATCH'])
@requires_auth('patch:drinks')
def patch_drinks(jwt, id):
   
#    drink = Drink.query.get(drink_id)
    drink_detail = Drink.query.filter(Drink.id==id).one_or_none()
    if drink_detail is None:
      abort(404)
   
    drink_recipe = []
  
    data = request.json
    
    if 'title' in data:
        drink_detail.title = data['title']
        
    if 'recipe' in data:
       for ingredient in body['recipe']:
            ingredient_name = ingredient['name']
            ingredient_color = ingredient['color']
            ingredient_parts = ingredient['parts']
            drink_recipe.append({
                'name': ingredient_name,
                'color': ingredient_color,
                'parts': ingredient_parts
            }) 
        
    json_drink_recipe = json.dumps(drink_recipe)
    drink_detail.recipe = json_drink_recipe

    drink_detail.update()

    return (  jsonify ({
          'success' : True,
          "drinks": [drink_detail.long()]
       }),
       200 
       )
      
  

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods = ['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(jwt, id):
   

   drink_detail = Drink.query.filter(Drink.id==id).one_or_none()
   if drink_detail is None:
      abort(404)
   
   try:
        drink_detail.delete()

        return ( jsonify ({
          'success' : True,
          "delete": id
       }),
       200 
        )
   except:
        abort(400)

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
def not_found(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(AuthError)
def authentication_error(err):
    return jsonify({
        'success': False,
        'error': err.status_code,
        'message': err.error
    }), err.status_code

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
                    "success": False, 
                    "error": 401,
                    "message": "User not authorized"
                    }), 401
