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

create_test_user()  # Create test user. Okay as API does not allow duplicates


def create_test_recipe():
    """ Create a test recipe, via an API endpoint """
    recipe_data = {
        "user_id"   : retrieve_test_user().get('id'),
        "title"     : "Tender Italian Baked chicken",
        "description": "This baked chicken recipe is ready in just 10 minutes",
        "fulfilled" : False
    }
    req = requests.post(
        recipe_list_url, json=recipe_data, headers=prepare_auth_headers()
    )
    return req


def test_recipe_creation():
    """ It should create a new recipe """
    req = create_test_recipe()
    assert req.status_code == 201


def test_recipe_attributes():
    """ Check that expected user attributes are returned """
    recipe_attributes = (
        "id",
        "user_id",
        "title",
        "description",
        "created",
        "modified",
        "links",
    )
    fetched_recipe = requests.get(
        recipe_list_url, headers=prepare_auth_headers()
    ).json()[0]
    for attr in recipe_attributes:
        assert attr in fetched_recipe.keys()


def test_recipe_list_pagination():
    """ It should return paginated list of recipes """
    limit = 1
    url = 'http://127.0.0.1:5000/recipes/?limit={}'.format(limit)
    auth_headers = prepare_auth_headers()
    req = requests.get(url, headers=auth_headers)

    assert req.status_code == 200
    assert req.json().__len__() == limit


def test_recipe_search():
    """ It should return recipes matching a given search criteria """
    search_term = "aked"
    url = 'http://127.0.0.1:5000/search/recipes?q={}'.format(search_term)
    auth_headers = prepare_auth_headers()
    req = requests.get(url, headers=auth_headers)
    assert req.status_code == 200
    recipes = req.json()
    assert len(recipes) > 0  # Because we know the recipe matching this exists

    search_term2 = "zqd"
    url2 = 'http://127.0.0.1:5000/search/recipes?q={}'.format(search_term2)
    req = requests.get(url2, headers=auth_headers)
    assert req.status_code == 200
    users2 = req.json()
    assert len(users2) == 0  # Because we know a user matching this exists


def test_recipe_deletion():
    """ It should delete a recipe and all its instructions and
    ingredients
    """
    recipe_list_url = 'http://127.0.0.1:5000/recipes/'
    auth_headers = prepare_auth_headers()
    recipes = requests.get(recipe_list_url, headers=auth_headers)

    recipe_id = recipes.json()[-1].get('id')  # Last Recipe's ID
    deletion_url = 'http://127.0.0.1:5000/recipes/{}/'.format(recipe_id)
    req = requests.delete(deletion_url, headers=auth_headers)
    assert req.status_code == 200  # FIXME: should be 204


delete_test_user()
