from models import (
    User
)


def test_default_attributes():
    assert User.__tablename__ is not None


def test_user_create():
    """ It should create a new user """
    first_name  = 'First'
    last_name   = 'Name'
    username    = 'username'
    email       = 'email@anonmail.com'
    password    = 'weakpass'

    user = User(
        first_name=first_name,
        last_name=last_name,
        username=username,
        email=email,
        password=password
    )

    assert user.first_name == first_name
    assert user.last_name == last_name
    assert user.username == username
    assert user.email ==  email
    assert user.password == password
