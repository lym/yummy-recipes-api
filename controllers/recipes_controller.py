from flask import (
    abort,
    request,
    jsonify,
)
from flask.views import MethodView

from models import (
    Recipe,
    User,
)
from models.base_model import db as DB
from .base_controller import (
    BaseController,
    RecipesEndpoint,
)


class RecipesController(MethodView):
    """ Controller for the recipe resource
    Any User can create a resource but a User can only GET/DELETE/PUT/PATCH
    a recipe that they own
    """
    def post(self):
        if not BaseController.authorized(request):
            abort(401)

        """ Recipe Creation """
        user_id = int(request.get_json().get('user_id'))
        title   = request.get_json().get('title')
        description = request.get_json().get('description')
        fulfilled   = request.get_json().get('fulfilled')

        # Check for required fields
        if user_id is None:
            abort(400, 'Please attach a user to this recipe')

        # Check if recipe owner exists
        existant_user = User.query.filter_by(id=user_id).first()
        if existant_user is None:
            print('Recipe owner does not exist!')
            res = jsonify({'status': 400})
            abort(res)

        # Check if recipe owner is originator of request
        req_token = BaseController.get_auth_token(request)
        token_owner = User.query.filter_by(auth_token=req_token).first()
        if user_id != token_owner.id:
            abort(400, 'Recipe owner/Token owner mismatch')

        # Check if recipe already exists
        existant_recipe = Recipe.query.filter_by(title=title.lower()).first()
        if ((existant_recipe is not None)and
                (existant_recipe.title == title.lower)):
            print('Recipe Already exists')
            res = jsonify({'status': 400})
            abort(res)
        new_recipe = Recipe(
            user_id=user_id,
            title=title,
            description=description,
            fulfilled=fulfilled
        )
        DB.session.add(new_recipe)
        DB.session.commit()
        res = {'status': 201}
        return jsonify(res)

    def get(self):
        if not BaseController.authorized(request):
            abort(401)
        user_token = BaseController.get_auth_token(request)
        if user_token is None:
            abort(401)
        user = User.query.filter_by(auth_token=user_token).first()

        """ Recipe retrieval """
        recipes = Recipe.query.filter_by(user_id=user.id)
        content = []
        for recipe in recipes:
            record = {
                'id': recipe.id,
                'user_id': recipe.user.id,
                'title': recipe.title,
                'description': recipe.description,
                'created': recipe.created,
                'modified': recipe.modified,
                'links': {
                    'self': RecipesEndpoint + str(recipe.id) + '/'
                }
            }
            content.append(record)
        res = jsonify(content)
        return res
