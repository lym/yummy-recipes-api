import requests

""" Note that to keep the test database in a clean state, we must always have
a test the deletes all that was created at the end of the test suite as is the
case currently.
"""

user_list_url = 'http://127.0.0.1:5000/users/'


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


def test_user_registration():
    """ It should create a new user """
    req = create_test_user()
    assert req.status_code == 200  # FIXME: This should be a 201


def test_user_attributes():
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


def test_user_list_pagination():
    """ It should return paginated list of users """
    limit = 1
    url = 'http://127.0.0.1:5000/users/?limit={}'.format(limit)
    auth_headers = prepare_auth_headers()
    req = requests.get(url, headers=auth_headers)

    assert req.status_code == 200
    assert req.json().__len__() == limit


def test_user_search():
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


def test_user_deletion():
    """ It should delete a user and all their recipes, instructions and
    ingredients
    """
    user_list_url = 'http://127.0.0.1:5000/users/'
    auth_headers = prepare_auth_headers()
    users = requests.get(user_list_url, headers=auth_headers)

    user_id = users.json()[-1].get('id')  # Last User's ID
    deletion_url = 'http://127.0.0.1:5000/users/{}/'.format(user_id)
    req = requests.delete(deletion_url, headers=auth_headers)
    assert req.status_code == 200  # FIXME: should be 204
