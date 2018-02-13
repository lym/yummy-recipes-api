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
from models.base_model import db as DB
from .base_controller import (
    BaseController,
    RecipesEndpoint,
)


class RecipesShowController(Resource):
    """ Handles requests for a single recipe entity """

    def _get_user_id_from_token(self, token):
        user = User.query.filter_by(auth_token=token).first()
        return user.id

    def _process_form_data(self, req_data, recipe):
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
            abort(res, 'Unauthorized Token')

        # Check if recipe owner is originator of request
        # Compare token in header to token submitted with data
        req_token = BaseController.get_auth_token(request)  # Grab from header
        if user_id != req_token:
            abort(400, 'Recipe owner/Token owner mismatch')

        '''
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
            'created': saved_recipe.created.strftime('%Y-%m-%d %H:%M:%S'),
            'modified': saved_recipe.modified,
        }
        '''

        if user_id is not None:
            recipe.user_id = self._get_user_id_from_token(user_id)
            DB.session.commit()
        if title is not None:
            recipe.title = title
            DB.session.commit()
        if description is not None:
            recipe.description = description
            DB.session.commit()
        recipe = Recipe.query.filter_by(id=recipe.id).first()
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
                'self': RecipesEndpoint + str(recipe.id) + '/'

            }
        }
        return record

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

        if request.form is not None:  # form-encoded string
            record = self._process_form_data(request.form, recipe)
            return record, 200

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
        return {'message': 'Recipe deleted'}, 200
