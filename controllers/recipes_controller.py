from flask import (
    abort,
    request,
    jsonify,
)
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from models import (
    Recipe,
    User,
)
from .base_controller import (
    BaseController,
    RecipesEndpoint,
)


class RecipesController(Resource):
    """ Controller for the recipe resource
    Any User can create a resource but a User can only GET/DELETE/PUT/PATCH
    a recipe that they own
    """
    def _get_user_id_from_token(self, token):
        user = User.query.filter_by(auth_token=token).first()
        return user.id

    def _process_form_data(self, req_data):
        """ Handles processing of records incase the recipe data is being
        submitted via a form-encoded data structure.
        Note that form data requests specify the owner of the recipe by
        submitting the owner's token so we need to look up the owner's user
        instance given their token.
        """
        user_id = req_data.get('user_id')
        title   = req_data.get('title')
        description = req_data.get('description')
        fulfilled   = req_data.get('fulfilled')

        # Check for required fields
        if user_id is None:
            abort(400, 'Please attach a user to this recipe')

        # Check if recipe owner exists
        existant_user = User.query.filter_by(auth_token=user_id).first()
        if existant_user is None:
            res = jsonify({'status': 400})
            abort(res)

        # Check if recipe owner is originator of request
        # Compare token in header to token submitted with data
        req_token = BaseController.get_auth_token(request)  # Grab from header
        if user_id != req_token:
            abort(400, 'Recipe owner/Token owner mismatch')

        try:
            new_recipe = Recipe(
                user_id=existant_user.id,
                title=title,
                description=description,
                fulfilled=fulfilled
            )
            new_recipe.save()
        except IntegrityError:
            abort(400, 'Possibly duplicate recipe!')
        saved_recipe = Recipe.query.filter_by(title=title).first()
        result = {
            'id': saved_recipe.id,
            'user_id': saved_recipe.user_id,
            'title': saved_recipe.title,
            'description': saved_recipe.description,
            'fulfilled': saved_recipe.fulfilled,
            'created': saved_recipe.created,
            'modified': saved_recipe.modified,
        }
        return result

    def _process_raw_json_data(self, req_data):
        """ Handles processing of records incase the recipe data is being
        submitted as a raw JSON string
        @req_data: The request payload object
        """
        user_token  = request.headers.get('Authorization').split(sep=' ')[-1]
        user_id     = self._get_user_id_from_token(user_token)
        title       = req_data.get('title')
        description = req_data.get('description')
        fulfilled   = req_data.get('fulfilled')

        # Check for required fields
        if title is None or len(title) == 0:  # Nonexistant or empty
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

        try:
            new_recipe = Recipe(
                user_id=existant_user.id,
                title=title,
                description=description,
                fulfilled=fulfilled
            )
            new_recipe.save()
        except IntegrityError:
            abort(400, 'Possibly duplicate recipe!')
        # TODO: Set 201 in header and return created item, like github does it
        saved_recipe = Recipe.query.filter_by(title=title).first()
        result = {
            'id': saved_recipe.id,
            'user_id': saved_recipe.user_id,
            'title': saved_recipe.title,
            'description': saved_recipe.description,
            'fulfilled': saved_recipe.fulfilled,
            'created': saved_recipe.created.strftime('%Y-%m-%d %H:%M:%S'),
            'modified': saved_recipe.modified,
        }
        return result

    def post(self):
        if not BaseController.authorized(request):
            abort(401)

        if request.get_json() is not None:  # Raw JSON string payload
            res = self._process_raw_json_data(request.get_json())
        elif request.form is not None:  # form-encoded string
            res = self._process_form_data(request.form)

        return res, 201

    def get(self):
        if not BaseController.authorized(request):
            abort(401, 'Please supply Authentication credentials')
        user_token = BaseController.get_auth_token(request)
        if user_token is None:
            abort(401, 'Bad User token supplied!')
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
        res = jsonify(results=content, status=201)
        return res
