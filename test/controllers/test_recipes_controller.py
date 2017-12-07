import unittest
import requests

from .helper import (
    create_test_user,
    delete_test_user,
    prepare_auth_headers,
    retrieve_test_user,
)

""" Note that to keep the test database in a clean state, we must always have
code that deletes all that was created at the end of the test suite as is the
case currently with delete_test_user().
"""

recipe_list_url = 'http://127.0.0.1:5000/recipes/'


class TestRecipesController(unittest.TestCase):
    def setUp(self):
        create_test_user()

    def tearDown(self):
        delete_test_user()

    def create_test_recipe(self):
        """ Create a test recipe, via an API endpoint """
        recipe_data = {
            "title"     : "Tender Italian Baked chicken",
            "description": "This baked chicken recipe is ready in just 10 minutes",
            "fulfilled" : False
        }
        req = requests.post(
            recipe_list_url, json=recipe_data, headers=prepare_auth_headers()
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
        requests.post(
            recipe_list_url, json=recipe_data, headers=prepare_auth_headers()
        )
        req = requests.get(recipe_list_url, headers=prepare_auth_headers())
        return req

    def delete_test_recipe(self):
        recipe_list_url = 'http://127.0.0.1:5000/recipes/'
        auth_headers    = prepare_auth_headers()
        recipes         = requests.get(recipe_list_url, headers=auth_headers)
        recipe_id       = recipes.json()[-1].get('id')  # Last Recipe's ID
        deletion_url    = 'http://127.0.0.1:5000/recipes/{}/'.format(recipe_id)
        requests.delete(deletion_url, headers=auth_headers)


    def test_recipe_creation(self):
        """ It should create a new recipe """
        req = self.create_test_recipe()
        assert req.status_code == 201


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
        fetched_recipes = requests.get(
            recipe_list_url, headers=prepare_auth_headers()
        ).json()
        for attr in recipe_attributes:
            assert attr in fetched_recipes.get('results')[0].keys()


    def test_recipe_list_pagination(self):
        """ It should return paginated list of recipes """
        self.create_two_test_recipes()
        limit        = 2
        url          = 'http://127.0.0.1:5000/recipes/?limit={}'.format(limit)
        auth_headers = prepare_auth_headers()
        req          = requests.get(url, headers=auth_headers)

        assert req.status_code == 200
        assert req.json().get('results').__len__() == limit


    def test_recipe_search(self):
        """ It should return recipes matching a given search criteria """
        self.create_test_recipe()
        search_term  = "aked"
        url          = 'http://127.0.0.1:5000/search/recipes?q={}'.format(
            search_term
        )
        auth_headers = prepare_auth_headers()
        req = requests.get(url, headers=auth_headers)
        assert req.status_code == 200
        recipes = req.json()
        assert len(recipes) > 0  # Because we know the recipe matching this exists

        search_term2 = "zqd"
        url2         = 'http://127.0.0.1:5000/search/recipes?q={}'.format(
            search_term2
        )
        req          = requests.get(url2, headers=auth_headers)
        assert req.status_code == 200
        users2 = req.json()
        assert len(users2) == 0  # Because we know a user matching this exists


    def test_recipe_deletion(self):
        """ It should delete a recipe and all its instructions and
        ingredients
        """
        self.create_test_recipe()
        recipe_list_url = 'http://127.0.0.1:5000/recipes/'
        auth_headers    = prepare_auth_headers()
        recipes         = requests.get(recipe_list_url, headers=auth_headers)
        recipe_id       = recipes.json().get('results')[-1].get('id')  # Last Recipe's ID NOQA
        deletion_url    = 'http://127.0.0.1:5000/recipes/{}/'.format(recipe_id)
        req             = requests.delete(deletion_url, headers=auth_headers)
        assert req.status_code == 204  # FIXME: should be 204
