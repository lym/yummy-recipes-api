from flask import (
    abort,
    request,
    jsonify,
)

from flask_restful import Resource

from models import (
    Instruction,
    Recipe,
)
from models.base_model import db as DB
from .base_controller import BaseController


class InstructionsController(Resource):
    """ Controller for the instructions resource
    A User may only add instructions to recipes that they own.
    """
    def post(self):
        if not BaseController.authorized(request):
            abort(401)

        if request.get_json() is None:
            abort(400, 'Please supply instruction record as JSON')

        """ Instruction Creation """
        recipe_id_str = request.get_json().get('recipe_id')

        # Check for required fields
        if recipe_id_str is None:
            abort(400, 'An instruction must be associated with a recipe')

        recipe_id = int(recipe_id_str)
        title       = request.get_json().get('title')
        description = request.get_json().get('description')

        # Check if recipe for instruction exists
        existant_recipe = Recipe.query.filter_by(id=recipe_id).first()
        if existant_recipe is None:
            abort(400, 'The recipe attached to instruction does not exist!')

        # Check if recipe attached to request belongs to the requester
        if not BaseController.authorized_and_owns_recipe(request, recipe_id):
            abort(401)

        # Check if instruction already exists
        existant_instruction = Instruction.query.filter_by(
            title=title.lower()
        ).first()
        if ((existant_instruction is not None) and
                (existant_instruction.title == title.lower) and
                existant_instruction.recipe_id == recipe_id):
            abort(400, 'Instruction already exists')
        new_instruction = Instruction(
            recipe_id=recipe_id,
            title=title,
            description=description,
        )
        DB.session.add(new_instruction)
        DB.session.commit()
        created_instruction = Instruction.query.filter_by(title=title).first()
        record = {
            'id': created_instruction.id,
            'recipe_id': created_instruction.recipe.id,
            'user_id': created_instruction.recipe.user.id,
            'title': created_instruction.title,
            'description': created_instruction.description,
            'created': created_instruction.created.strftime('%Y-%m-%d %H:%M:%S'),  # NOQA
        }
        return record, 201

    def get(self):
        if not BaseController.authorized(request):
            abort(401)

        """ Recipe retrieval """
        instructions = Instruction.query.all()
        content = []
        for instruction in instructions:
            record = {
                'id': instruction.id,
                'recipe_id': instruction.recipe.id,
                'user_id': instruction.recipe.user.id,
                'title': instruction.title,
                'description': instruction.description,
                'created': instruction.created,
                'modified': instruction.modified
            }
            content.append(record)
        res = jsonify(content)
        return res
