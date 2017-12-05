from flask import (
    abort,
    request,
    jsonify,
)
from flask_restful import Resource

from models import (
    Recipe,
    User,
)
from .base_controller import (
    BaseController,
    RecipesEndpoint,
)


class UserRecipeController(Resource):
    """ Handles requests for a single recipe entity """
    def get(self, user_id, recipe_id):
        print('User ID: {}\nRecipe ID: {}'.format(user_id, recipe_id))
        if not BaseController.authorized(request):
            abort(401, 'Please supply authentication credentials')
        user_id = int(user_id)
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            return {'message': 'Ooops! requested user does not exist'}, 404

        recipe_id = int(recipe_id)
        """
        recipe = Recipe.query.filter_by(id=recipe_id).first()
        if recipe is None:
            abort(404, 'Requested recipe does not exist on the server')
        """
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
