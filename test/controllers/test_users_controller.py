import json
from flask_testing import TestCase
import requests

from app import app

from .helper import (
    create_test_user,
    delete_test_user,
    create_passwordless_user,
    prepare_auth_headers,
    prepare_fake_auth_headers,
)

""" Note that to keep the test database in a clean state, we must always have
a test the deletes all that was created at the end of the test suite as is the
case currently.
"""

user_list_url = 'http://127.0.0.1:5000/users/'


class TestUsersController(TestCase):
    def create_app(self, app=app):
        app.config.from_object('settings.TestEnv')
        return app

    def setUp(self):
        self.users_url = 'http://127.0.0.1:5000/users/'
        self.req = create_test_user()

    def tearDown(self):
        delete_test_user()

    """
    def test_user_registration(self):
        # It should create a new user
        delete_test_user()
        req = self.req
        if (req.status_code == 400 and
                req.json().get('message') == 'User already exists!'):
            delete_test_user()
            req = create_test_user()
        assert req.status_code == 201
        assert req.json().__len__() != 0
     """

    def test_create_duplicate_user(self):
        """ It should deny creation of duplicate users """
        req = create_passwordless_user()
        assert req.status_code == 400
        assert req.json()['message'] == 'Please enter a valid password'

    def test_create_user_with_missing_username_attribute(self):
        """ It should allow creation of a user with a missing first_name
        attribute
        """
        user_credentials = {
            "last_name" : "Dinara",
            "email"     : "dsafina@wta.com",
            "username"  : "dsafina",
            "password"  : "testpass"
        }
        req = self.client.post(
            self.users_url,  data=json.dumps(user_credentials),
            content_type='application/json',
            headers=prepare_auth_headers()
        )
        self.assertEqual(req.status_code, 201)
        self.assertNotEqual(len(req.json), 0)
        self.assertIn('links', req.json.keys())

    def test_create_user_with_invalid_email_address(self):
        """ An attempt to create a user with an invalid email address should be
        blocked.
        """
        user_credentials = {
            "email"     : "dsafinawta.com",
            "username"  : "dsafina",
            "password"  : "testpass"
        }
        req = self.client.post(
            self.users_url,  data=json.dumps(user_credentials),
            content_type='application/json',
            headers=prepare_auth_headers()
        )
        self.assertEqual(req.status_code, 400)
        self.assertIn('Please valid email address',
            req.json.get('message')
        )

    def test_create_user_with_no_password(self):
        """ An attempt to create a user without the password attribute should
        be blocked.
        """
        user_credentials = {
            "email"     : "dsafinawta.com",
            "username"  : "dsafina",
            "password"  : ""
        }
        req = self.client.post(
            self.users_url,  data=json.dumps(user_credentials),
            content_type='application/json',
            headers=prepare_auth_headers()
        )
        self.assertEqual(req.status_code, 400)
        self.assertEqual('Please enter a valid password',
            req.json.get('message')
        )

    def test_create_user_with_invalid_username(self):
        """ An attempt to create a user with an invalid username should be
        blocked.
        """
        user_credentials = {
            "email"     : "dsafina@wta.com",
            "username"  : 123,
            "password"  : "testpass"
        }
        req = self.client.post(
            self.users_url,  data=json.dumps(user_credentials),
            content_type='application/json',
            headers=prepare_auth_headers()
        )
        self.assertEqual(req.status_code, 400)
        self.assertIn('Please supply valid username',
            req.json.get('message')
        )

    def test_create_user_with_no_user_records(self):
        """ An attempt to create a user record without supplying any attributes
        should be blocked.
        """
        user_credentials = None
        req = self.client.post(
            self.users_url,  data=json.dumps(user_credentials),
            content_type='application/json',
            headers=prepare_auth_headers()
        )
        self.assertEqual(req.status_code, 400)
        self.assertIn('Please supply user credentials as JSON',
            req.json.get('message')
        )

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

    def test_retrieve_single_user(self):
        users = self.client.get(
            user_list_url,
            content_type='application/json',
            headers=prepare_auth_headers()
        )
        # if users.json.__len__() == 0 or users.status_code == 401:
        #   return 0
        user_id = users.json[-1].get('id')  # Last User's ID
        user_url = 'http://127.0.0.1:5000/users/{}/'.format(user_id)
        user = self.client.get(
            user_url,
            content_type='application/json',
            headers=prepare_auth_headers()
        )
        self.assertEqual(user.status_code, 200)
        self.assertGreater(user.json.__len__(), 0)
        self.assertIn('email', user.json.keys())

    def test_retrive_non_existant_user(self):
        """ An attempt to retrieve a non-existant user should be greeted with
        a 404.
        """
        user_id = 1000000  # Since we are fairly sure this user does not exist
        user_url = 'http://127.0.0.1:5000/users/{}/'.format(user_id)
        user = self.client.get(
            user_url,
            content_type='application/json',
            headers=prepare_auth_headers()
        )
        self.assertEqual(user.status_code, 404)
        self.assertNotIn('email', user.json.keys())
        self.assertIn('User not found', user.json.get('message'))

    def test_retrieve_user_with_invalid_auth_credentials(self):
        """ An attempt by an unauthorized user to retrieve a user should be
        blocked.
        """
        user_id = 1000000  # Since we are fairly sure this user does not exist
        user_url = 'http://127.0.0.1:5000/users/{}/'.format(user_id)
        user = self.client.get(
            user_url,
            content_type='application/json',
            headers=prepare_fake_auth_headers()
        )
        self.assertEqual(user.status_code, 401)
        self.assertNotIn('email', user.json.keys())
        self.assertIn(
            'Please supply authentication credentials',
            user.json.get('message')
        )

    def test_user_list_pagination(self):
        """ It should return paginated list of users """
        limit = 1
        url = 'http://127.0.0.1:5000/users/?limit={}'.format(limit)
        auth_headers = prepare_auth_headers()
        req = self.client.get(
            url, content_type='application/json', headers=auth_headers
        )

        assert req.status_code == 200
        assert req.json.__len__() == limit

    def test_user_search(self):
        """ It should return users matching a given search criteria """
        search_term = "fin"
        url = 'http://127.0.0.1:5000/search/users?q={}'.format(search_term)
        auth_headers = prepare_auth_headers()
        req = self.client.get(
            url, content_type='application/json', headers=auth_headers
        )
        assert req.status_code == 200
        users = req.json
        assert len(users) > 0  # Because we know a user matching this exists

        search_term2 = "zqd"
        url2 = 'http://127.0.0.1:5000/search/users?q={}'.format(search_term2)
        req = self.client.get(
            url2, content_type='application/json', headers=auth_headers
        )
        assert req.status_code == 200
        users2 = req.json
        assert len(users2) == 0  # Because we know a user matching this exists

    def test_user_deletion(self):
        """ It should delete a user and all their recipes, instructions and
        ingredients
        FIXME: Token in auth_headers does not appear to match user that is being
        deleted
        """
        """
        user_list_url = 'http://127.0.0.1:5000/users/'
        auth_headers = prepare_auth_headers()
        user = self.req
        if (user.status_code == 400 and
                user.json().get('message') == 'User already exists!'):
            user = self.client.get(
                self.users_url, content_type='application/json', headers=auth_headers
            )


        user_id = user.json[-1].get('id')
        deletion_url = 'http://127.0.0.1:5000/users/{}/'.format(user_id)
        req = self.client.delete(deletion_url, headers=auth_headers)
        assert req.status_code == 204
        """
        """
        self.assertEqual(
            req.json.get('message'),
            'User Deleted'
        )
        """

        """ Implementation 2
        user_list_url   = 'http://127.0.0.1:5000/users/'
        auth_headers    = prepare_auth_headers()
        users           = self.client.get(
            user_list_url,
            content_type='application/json',
            headers=auth_headers
        )
        # if users.json.__len__() == 0 or users.status_code == 401:
        #   return 0
        user_id = users.json[-1].get('id')  # Last User's ID
        deletion_url = 'http://127.0.0.1:5000/users/{}/'.format(user_id)
        req = self.client.delete(deletion_url, headers=auth_headers)
        assert req.status_code == 204
        """
