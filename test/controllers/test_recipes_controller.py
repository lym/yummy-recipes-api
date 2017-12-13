import json
from flask_testing import TestCase

from app import app

from .helper import (
    create_test_user,
    delete_test_user,
    prepare_auth_headers,
    prepare_fake_auth_headers,
)

""" Note that to keep the test database in a clean state, we must always have
code that deletes all that was created at the end of the test suite as is the
case currently with delete_test_user().
"""

recipe_list_url = 'http://127.0.0.1:5000/recipes/'


class TestRecipesController(TestCase):
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

    def test_valid_recipe_creation(self):
        """ It should create a new recipe """
        req = self.create_test_recipe()
        assert req.status_code == 201

    def test_create_recipe_without_title(self):
        """ An attempt to create a recipe without a title attribute should be
        blocked.
        """
        recipe_data = {
            "description": "This recipe has no title",  # NOQA
            "fulfilled" : False
        }
        req = self.client.post(
            recipe_list_url, data=json.dumps(recipe_data),
            content_type='application/json',
            headers=prepare_auth_headers()
        )
        self.assertEqual(req.status_code, 400)
        self.assertEqual(
            req.json.get('message'),
            'Please attach a user to this recipe'
        )

    def test_create_recipe_by_unauthorized_user(self):
        """ An attempt by an unauthorized user to create a recipe should be
        blocked.
        """
        recipe_data = {
            "title": "This a recipe by an invalid user",
            "description": "This recipe has no title",  # NOQA
            "fulfilled" : True
        }
        req = self.client.post(
            recipe_list_url, data=json.dumps(recipe_data),
            content_type='application/json',
            headers=prepare_fake_auth_headers()
        )
        self.assertEqual(req.status_code, 401)
        self.assertEqual(
            req.json.get('message'),
            'You are not Authorized to access this resource'
        )

    def test_fetch_recipe_by_unauthorized_user(self):
        """ An attempt by an unauthorized user to fetch a recipe should be
        blocked.
        """
        self.create_test_recipe()
        recipe_list_url = 'http://127.0.0.1:5000/recipes/'
        auth_headers    = prepare_fake_auth_headers()
        req         = self.client.get(
            recipe_list_url, content_type='application/json',
            headers=auth_headers
        )
        self.assertEqual(req.status_code, 401)
        self.assertEqual(
            req.json.get('message'),
            'You are not Authorized to access this resource'
        )

    def test_recipe_attributes(self):
        """ Check that expected user attributes are returned """
        self.create_test_recipe()
        recipe_attributes = (
            "id",
            "user_id",
            "title",
            "description",
            "created",
            "modified",
            "links",
        )
        fetched_recipes = self.client.get(
            recipe_list_url,
            content_type='application/json',
            headers=prepare_auth_headers()
        ).json
        for attr in recipe_attributes:
            assert attr in fetched_recipes.get('results')[0].keys()

    def test_recipe_list_pagination(self):
        """ It should return paginated list of recipes """
        self.create_two_test_recipes()
        limit        = 2
        url          = 'http://127.0.0.1:5000/recipes/?limit={}'.format(limit)
        auth_headers = prepare_auth_headers()
        req          = self.client.get(
            url, content_type='application/json', headers=auth_headers
        )

        assert req.status_code == 200
        assert req.json.get('results').__len__() == limit

    def test_recipe_search(self):
        """ It should return recipes matching a given search criteria """
        self.create_test_recipe()
        search_term  = "aked"
        url          = 'http://127.0.0.1:5000/search/recipes?q={}'.format(
            search_term
        )
        auth_headers = prepare_auth_headers()
        req = self.client.get(
            url, content_type='application/json', headers=auth_headers
        )
        assert req.status_code == 200
        recipes = req.json
        assert len(recipes) > 0  # Because we know the recipe matching this exists  # NOQA

        search_term2 = "zqd"
        url2         = 'http://127.0.0.1:5000/search/recipes?q={}'.format(
            search_term2
        )
        req          = self.client.get(
            url2, content_type='application/json', headers=auth_headers
        )
        assert req.status_code == 200
        users2 = req.json
        assert len(users2) == 0  # Because we know a user matching this exists

    def test_recipe_deletion(self):
        """ It should delete a recipe and all its instructions and
        ingredients
        """
        self.create_test_recipe()
        recipe_list_url = 'http://127.0.0.1:5000/recipes/'
        auth_headers    = prepare_auth_headers()
        recipes         = self.client.get(
            recipe_list_url, content_type='application/json',
            headers=auth_headers
        )
        recipe_id       = recipes.json.get('results')[-1].get('id')  # Last Recipe's ID  # NOQA
        deletion_url    = 'http://127.0.0.1:5000/recipes/{}/'.format(recipe_id)
        req             = self.client.delete(
            deletion_url, headers=auth_headers
        )
        assert req.status_code == 204  # FIXME: should be 204
