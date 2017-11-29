from flask import (
    abort,
    request,
    jsonify,
)
from flask_restful import Resource

from models import Recipe
from models.base_model import db as DB
from .base_controller import (
    BaseController,
    RecipesEndpoint,
)


class RecipesShowController(Resource):
    """ Handles requests for a single recipe entity """
    def get(self, recipe_id):
        if not BaseController.authorized(request):
            abort(401, 'Please supply authentication credentials')
        recipe_id = int(recipe_id)
        recipe = Recipe.query.filter_by(id=recipe_id).first()
        if recipe is None:
            abort(404, 'Requested recipe does not exist on the server')
        record = {
            'id': recipe.id,
            'title': recipe.title,
            'description': recipe.description,
            'fulfilled': recipe.fulfilled,
            'user_id': recipe.user.id,
            'user': recipe.user.username,
            'created': recipe.created,
            'modified': recipe.modified,
            'links': {
                'self': RecipesEndpoint + str(recipe_id) + '/'

            }
        }
        res = jsonify(record)
        return res

    def patch(self, recipe_id):
        """ Update/Edit user data """
        if not BaseController.authorized(request):
            abort(401, 'Please supply valid user credentials')
        recipe_id = int(recipe_id)
        recipe = Recipe.query.filter_by(id=recipe_id).first()
        if recipe_id is None:
            abort(404, 'Requested recipe does not exist on the server')

        # Ensure a user is updating their own recipe record
        curr_user = BaseController.auth_user(request)
        if recipe.user.id != curr_user.id:
            abort(403, 'A user can only update their recipe records!')

        user_id = request.get_json().get('user_id')
        title = request.get_json().get('title')
        description = request.get_json().get('description')

        if user_id is not None:
            recipe.user_id = user_id
            DB.session.commit()
        if title is not None:
            recipe.title = title
            DB.session.commit()
        if description is not None:
            recipe.description = description
            DB.session.commit()
        recipe = Recipe.query.filter_by(id=recipe_id).first()
        record = {
            'id': recipe.id,
            'title': recipe.title,
            'description': recipe.description,
            'fulfilled': recipe.fulfilled,
            'user_id': recipe.user.id,
            'user': recipe.user.username,
            'created': recipe.created.strftime('%Y-%m-%d %H:%M:%S'),
            'modified': recipe.modified.strftime('%Y-%m-%d %H:%M:%S'),
            'links': {
                'self': RecipesEndpoint + str(recipe_id) + '/'

            }
        }
        return record, 200

    def delete(self, recipe_id):
        """ Delete a recipe and all its instructions and ingredients """
        if not BaseController.authorized(request):
            abort(401, 'Please supply valid user credentials')
        recipe = Recipe.query.filter_by(id=recipe_id).first()
        if recipe is None:
            abort(404, 'Requested recipe does not exist on the server')

        # Ensure a user is deleting their own recipe record
        curr_user = BaseController.auth_user(request)
        if recipe.user.id != curr_user.id:
            abort(403, 'A user can only delete their recipe records!')
        instructions = recipe.instructions
        if instructions != []:
            for instruction in instructions:
                DB.session.delete(instruction)
                DB.session.commit()
        ingredients = recipe.ingredients
        if ingredients != []:
            for ingredient in ingredients:
                DB.session.delete(ingredient)
                DB.session.commit()
        DB.session.delete(recipe)
        DB.session.commit()
        return {'message': 'User deleted'}, 204
