import unittest
import requests

from .helper import (
    create_test_user,
    delete_test_user,
    create_passwordless_user,
    prepare_auth_headers,
)

""" Note that to keep the test database in a clean state, we must always have
a test the deletes all that was created at the end of the test suite as is the
case currently.
"""

user_list_url = 'http://127.0.0.1:5000/users/'


class TestUsersController(unittest.TestCase):
    def setUp(self):
        self.req = create_test_user()

    def tearDown(self):
        delete_test_user()

    def test_user_registration(self):
        """ It should create a new user """
        req = self.req
        if (req.status_code == 400 and
                req.json().get('message') == 'User already exists!'):
            delete_test_user()
            req = create_test_user()
        assert req.status_code == 201
        assert req.json().__len__() != 0


    def test_create_duplicate_user(self):
        """ It should deny creation of duplicate users """
        req = create_passwordless_user()
        assert req.status_code == 400
        assert req.json()['message'] == 'Please enter password'


    def test_create_user_with_missing_attribute(self):
        """ It should deny creation of a user with a missing user attribute """
        pass


    def test_user_attributes(self):
        """ Check that expected user attributes are returned """
        user_attributes = (
            "first_name",
            "last_name",
            "username",
            "email",
            "id",
            "email",
            "links",
        )
        fetched_user = requests.get(
            user_list_url, headers=prepare_auth_headers()
        ).json()[0]
        for attr in user_attributes:
            assert attr in fetched_user.keys()


    def test_user_list_pagination(self):
        """ It should return paginated list of users """
        limit = 1
        url = 'http://127.0.0.1:5000/users/?limit={}'.format(limit)
        auth_headers = prepare_auth_headers()
        req = requests.get(url, headers=auth_headers)

        assert req.status_code == 200
        assert req.json().__len__() == limit


    def test_user_search(self):
        """ It should return users matching a given search criteria """
        search_term = "fin"
        url = 'http://127.0.0.1:5000/search/users?q={}'.format(search_term)
        auth_headers = prepare_auth_headers()
        req = requests.get(url, headers=auth_headers)
        assert req.status_code == 200
        users = req.json()
        assert len(users) > 0  # Because we know a user matching this exists

        search_term2 = "zqd"
        url2 = 'http://127.0.0.1:5000/search/users?q={}'.format(search_term2)
        req = requests.get(url2, headers=auth_headers)
        assert req.status_code == 200
        users2 = req.json()
        assert len(users2) == 0  # Because we know a user matching this exists


    def test_user_deletion(self):
        """ It should delete a user and all their recipes, instructions and
        ingredients
        """
        # user_list_url = 'http://127.0.0.1:5000/users/'
        auth_headers = prepare_auth_headers()
        # users = requests.get(user_list_url, headers=auth_headers)
        user = self.req

        user_id = user.json().get('id')
        deletion_url = 'http://127.0.0.1:5000/users/{}/'.format(user_id)
        req = requests.delete(deletion_url, headers=auth_headers)
        assert req.status_code == 200  # FIXME: should be 204
