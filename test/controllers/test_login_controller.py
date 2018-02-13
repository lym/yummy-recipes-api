from flask_testing import TestCase
import json

from app import app

from .helper import (
    create_test_user,
    delete_test_user,
)


class TestLoginController(TestCase):
    def create_app(self, app=app):
        """ Initialize app"""
        app.config.from_object('settings.TestEnv')
        return app

    def setUp(self):
        create_test_user()
        self.login_url = 'http://127.0.0.1:5000/login/'

    def tearDown(self):
        delete_test_user()

    def test_valid_login(self):
        email     = "smarat@atptour.com"
        password  = "testpass"
        user_credentials = {'email': email, 'password': password}
        req = self.client.post(
            self.login_url, data=json.dumps(user_credentials),
            content_type='application/json'
        )
        self.assertEqual(req.status_code, 200)
        self.assertNotEqual(req.json.__len__(), 0)

    def test_invalid_login(self):
        """ An unregistered user should be denied access to the system """
        email     = "inv_user@invacc.com"
        password  = "testpass2"
        user_credentials = {'email': email, 'password': password}
        req = self.client.post(
            self.login_url, data=json.dumps(user_credentials),
            content_type='application/json'
        )
        self.assertEqual(req.status_code, 401)
        self.assertEqual(
            req.json.get('message'),
            'You are not Authorized to access this resource'
        )

    def test_login_user_with_no_email_attribute(self):
        """ An attempt to login a user with no email attribute should
        be blocked.
        """
        password  = "testpass"
        user_credentials = {'password': password}
        req = self.client.post(
            self.login_url, data=json.dumps(user_credentials),
            content_type='application/json'
        )

        self.assertEqual(req.status_code, 400)
        self.assertEqual(
            req.json.get('message'),
            'You need to supply an email address attribute'
        )

    def test_login_user_with_no_password_attribute(self):
        """ An attempt to login a user with no password attribute should
        be blocked.
        """
        email = "inv_user@invacc.com"
        user_credentials = {'email': email}
        req = self.client.post(
            self.login_url, data=json.dumps(user_credentials),
            content_type='application/json'
        )

        self.assertEqual(req.status_code, 400)
        self.assertEqual(
            req.json.get('message'),
            'You need to supply a password attribute'
        )

    def test_login_user_with_no_credentials(self):
        """ An attempt to login a user without both an email and a password
        should be blocked.
        """
        user_credentials = None
        req = self.client.post(
            self.login_url, data=json.dumps(user_credentials),
            content_type='application/json'
        )

        self.assertEqual(req.status_code, 400)
        self.assertEqual(
            req.json.get('message'),
            'Please supply email and password'
        )

    def test_login_user_with_wrong_password(self):
        """ An attempt to login a user with an existant email but wrong
        password should be blocked.
        """
        email     = "smarat@atptour.com"
        password  = "notmaratspass"
        user_credentials = {'email': email, 'password': password}
        req = self.client.post(
            self.login_url, data=json.dumps(user_credentials),
            content_type='application/json'
        )
        self.assertEqual(req.status_code, 401)
        self.assertNotEqual(req.json.__len__(), 0)
        self.assertEqual(
            req.json.get('message'),
            'You are not Authorized to access this resource'
        )

    def test_login_user_with_non_existant_email(self):
        """ An attempt to login a user with a non-existant email should be
        blocked.
        """
        email     = "notfound@atptour.com"
        password  = "notmaratspass"
        user_credentials = {'email': email, 'password': password}
        req = self.client.post(
            self.login_url, data=json.dumps(user_credentials),
            content_type='application/json'
        )
        self.assertEqual(req.status_code, 401)
        self.assertNotEqual(req.json.__len__(), 0)
        self.assertEqual(
            req.json.get('message'),
            'You are not Authorized to access this resource'
        )
