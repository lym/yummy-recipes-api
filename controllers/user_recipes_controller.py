from flask import (
    abort,
    request,
)
from flask_restful import Resource

from models import (
    User,
    Recipe,
)
from .base_controller import (
    BaseController,
    RecipesEndpoint,
)


class UserRecipesController(Resource):
    """ This controller handles requests for a user's recipe list. It handles
    requests of the form `GET /users/<user_id>/recipes/`
    """

    def _recipe_modified_date(self, modified_datetime):
        if modified_datetime is None:
            return None
        return modified_datetime.strftime('%Y-%m-%d %H:%M:%S %Z')

    def get(self, user_id):
        if not BaseController.authorized(request):
            abort(401, 'Please supply authentication credentials')
        user_id = int(user_id)
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            return {'message': 'Ooops! requested user does not exist'}, 404

        recipes = Recipe.query.filter_by(user_id=user.id)
        content = []
        for recipe in recipes:
            record = {
                'id': recipe.id,
                'title': recipe.title,
                'description': recipe.description,
                'fulfilled': recipe.fulfilled,
                'user_id': recipe.user.id,
                'user': recipe.user.username,
                'created': recipe.created.strftime('%Y-%m-%d %H:%M:%S %Z'),
                'modified': self._recipe_modified_date(recipe.modified),
                'links': {
                    'self': RecipesEndpoint + str(recipe.id) + '/'

                }
            }
            content.append(record)

        res = content, 200
        return res
