import requests

""" This module contains utility methods usable across all the controller test
cases.
"""


def create_test_user():
    """ Create a test user, via an API endpoint """
    url = 'http://127.0.0.1:5000/users/'
    user_credentials = {
        "first_name": "Safin",
        "last_name" : "Marat",
        "email"     : "smarat@atptour.com",
        "username"  : "smarat",
        "password"  : "testpass"
    }
    req = requests.post(url, json=user_credentials)
    return req


def retrieve_auth_token():
    """ It fetches a valid user authentication token, from the API server, to
    be used in the subsequent requests for protected resources.
    """
    login_url     = 'http://127.0.0.1:5000/login/'
    user_credentials = {
        "email"     : "smarat@atptour.com",
        "password"  : "testpass"
    }
    auth_token = requests.post(
        login_url, json=user_credentials
    ).json().get('token')
    return auth_token


def prepare_auth_headers():
    """ Creates the authentication headers dictionary for use with requests for
    protected resources.
    """
    auth_token = retrieve_auth_token()
    auth_headers = {
        'Authorization': 'Token {}'.format(auth_token)
    }
    return auth_headers


def retrieve_test_user():
    """ Fetches a user from the endpoint. This enables us to have access to
    user records like id, token, creation and modification dates that are only
    present after a user is created.
    """
    create_test_user()
    user_list_url = 'http://127.0.0.1:5000/users/'
    auth_headers = prepare_auth_headers()
    users = requests.get(user_list_url, headers=auth_headers)
    user = users.json()[-1]  # Last User
    return user


def delete_test_user():
    """ Delete the user created during the test run to ensure our database is
    left in a pristine state.
    """
    user_list_url = 'http://127.0.0.1:5000/users/'
    auth_headers = prepare_auth_headers()
    users = requests.get(user_list_url, headers=auth_headers)

    user_id = users.json()[-1].get('id')  # Last User's ID
    deletion_url = 'http://127.0.0.1:5000/users/{}/'.format(user_id)
    requests.delete(deletion_url, headers=auth_headers)
