import requests

""" Note that to keep the test database in a clean state, we must always have
a test the deletes all that was created at the end of the test suite as is the
case currently.
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


def test_user_registration():
    """ It should create a new user """
    req = create_test_user()
    assert req.status_code == 200  # FIXME: This should be a 201


def test_user_list_pagination():
    """ It should return paginated list of users """
    limit = 1
    url = 'http://127.0.0.1:5000/users/?limit={}'.format(limit)
    headers = {
        'Authorization': 'Token c198ecbca9af5bbe7ba50ec6a4f4df1ffbf5d004'
    }
    req = requests.get(url, headers=headers)

    assert req.status_code == 200
    assert req.json().__len__() == limit


def test_user_deletion():
    """ It should delete a user and all their recipes, instructions and
    ingredients
    """
    user_list_url = 'http://127.0.0.1:5000/users/'
    login_url     = 'http://127.0.0.1:5000/login/'
    user_credentials = {
        "email"     : "smarat@atptour.com",
        "password"  : "testpass"
    }
    auth_token = requests.post(
        login_url, json=user_credentials
    ).json().get('token')
    auth_headers = {
        'Authorization': 'Token {}'.format(auth_token)
    }
    users = requests.get(user_list_url, headers=auth_headers)

    user_id = users.json()[-1].get('id')  # Last User's ID
    deletion_url = 'http://127.0.0.1:5000/users/{}/'.format(user_id)
    req = requests.delete(deletion_url, headers=auth_headers)
    assert req.status_code == 200  # FIXME: should be 204
