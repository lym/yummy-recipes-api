from flask import (
    abort,
    request,
    jsonify,
)
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

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
            DB.session.add(new_recipe)
            DB.session.commit()
        except IntegrityError:
            print('Possibly duplicate recipe!')
            abort(400, 'Possibly duplicate recipe!')
        return {'status': 201}

    def _process_raw_json_data(self, req_data):
        """ Handles processing of records incase the recipe data is being
        submitted and a raw JSON string
        @req_data: The request payload object
        """
        user_id = int(req_data.get('user_id'))
        title   = req_data.get('title')
        description = req_data.get('description')
        fulfilled   = req_data.get('fulfilled')

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
        return {'status': 201}

    def post(self):
        if not BaseController.authorized(request):
            abort(401)

        if request.get_json() is not None:  # Raw JSON string payload
            res = self._process_raw_json_data(request.get_json())
        elif request.form is not None:  # form-encoded string
            res = self._process_form_data(request.form)

        return jsonify(res)

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
        res = jsonify(content)
        return res
