import json
from flask_testing import TestCase

from app import app

from .helper import (
    create_test_user,
    delete_test_user,
    prepare_auth_headers,
)

""" Note that to keep the test database in a clean state, we must always have
code that deletes all that was created at the end of the test suite as is the
case currently with delete_test_user().
"""

recipe_list_url = 'http://127.0.0.1:5000/recipes/'
instructions_url = 'http://127.0.0.1:5000/instructions/'


class TestInstructionsController(TestCase):
    def create_app(self, app=app):
        app.config.from_object('settings.TestEnv')
        return app

    def setUp(self):
        create_test_user()

    def tearDown(self):
        delete_test_user()

    def create_test_recipe(self):
        """ Create a test recipe, via an API endpoint """
        recipe_data = {
            "title"     : "Tender Italian Baked chicken",
            "description": "This baked chicken recipe is ready in just 10 minutes",  # NOQA
            "fulfilled" : False
        }
        req = self.client.post(
            recipe_list_url, data=json.dumps(recipe_data),
            content_type='application/json',
            headers=prepare_auth_headers()
        )
        return req

    def create_test_instruction(self):
        """ Creates an instruction object for testing purposes """
        recipe = self.create_test_recipe()
        recipe_id = recipe.json.get('id')
        instruction_record = {
            "recipe_id" : recipe_id,
            "title"     : "This instruction is for valid test recipe",
            "fulfilled"  : "false",
        }
        req = self.client.post(
            instructions_url, data=json.dumps(instruction_record),
            content_type='application/json',
            headers=prepare_auth_headers()
        )
        return req

    def create_two_test_recipes(self):
        """ This helper method creates two recipes for testing purposes. It
        should not be called, in the same sequence, with create_test_recipe()
        """
        self.create_test_recipe()
        recipe_data = {
            "title"     : "Creamy chicken with wild rice soup",
            "description": "Instant wild rice is cooked in chicken broth",
            "fulfilled" : False
        }
        self.client.post(
            recipe_list_url, data=json.dumps(recipe_data),
            content_type='application/json',
            headers=prepare_auth_headers()
        )
        req = self.client.get(
            recipe_list_url,
            content_type='application/json',
            headers=prepare_auth_headers()
        )
        return req

    def delete_test_recipe(self):
        recipe_list_url = 'http://127.0.0.1:5000/recipes/'
        auth_headers    = prepare_auth_headers()
        recipes         = self.client.get(
            recipe_list_url,
            content_type='application/json',
            headers=auth_headers
        )
        recipe_id       = recipes.json[-1].get('id')  # Last Recipe's ID
        deletion_url    = 'http://127.0.0.1:5000/recipes/{}/'.format(recipe_id)
        self.client.delete(
            deletion_url,
            headers=prepare_auth_headers()
        )

    def test_valid_instruction_creation(self):
        """ It should create a new recipe """
        recipe = self.create_test_recipe()
        recipe_id = recipe.json.get('id')
        instruction_record = {
            "recipe_id" : recipe_id,
            "title"     : "This instruction is for valid test recipe",
            "fulfilled"  : "false",
        }
        req = self.client.post(
            instructions_url, data=json.dumps(instruction_record),
            content_type='application/json',
            headers=prepare_auth_headers()
        )
        self.assertEqual(req.status_code, 201)
        self.assertNotEqual(len(req.json), 0)
        self.assertIn('title', req.json.keys())

    def test_create_instruction_without_recipe(self):
        """ An attempt to create an instruction without a recipe attached to it
        should be blocked.
        """
        instruction_record = {
            "title"     : "This instruction is for valid test recipe",
            "fulfilled"  : "false",
        }
        req = self.client.post(
            instructions_url, data=json.dumps(instruction_record),
            content_type='application/json',
            headers=prepare_auth_headers()
        )
        self.assertEqual(req.status_code, 400)
        self.assertNotEqual(len(req.json), 0)
        self.assertEqual(
            'An instruction must be associated with a recipe',
            req.json.get('message')
        )

    def test_create_instruction_attached_to_non_existant_recipe(self):
        """ An attempt to create an instruction whose recipe does not exist
        should be blocked.
        """
        instruction_record = {
            "recipe_id": 120000000,  # We assume this recipe is non-existant
            "title"     : "This instruction is for valid test recipe",
            "fulfilled"  : "false",
        }
        req = self.client.post(
            instructions_url, data=json.dumps(instruction_record),
            content_type='application/json',
            headers=prepare_auth_headers()
        )
        self.assertEqual(req.status_code, 400)
        self.assertNotEqual(len(req.json), 0)
        self.assertEqual(
            'The recipe attached to instruction does not exist!',
            req.json.get('message')
        )

    def test_retrieve_instruction(self):
        """ A user should be able to retrieve instructions """
        self.create_test_instruction()
        auth_headers    = prepare_auth_headers()
        req         = self.client.get(
            instructions_url, content_type='application/json',
            headers=auth_headers
        )
        self.assertEqual(req.status_code, 200)
        self.assertNotEqual(len(req.json), 0)
