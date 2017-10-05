from models import (
    User
)

from app import db as DB


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

    # Persist the user in the database
    DB.session.add(user)
    DB.session.commit()


def test_user_retrieval():  # Test got GET /endpoint/users/id/
    """ It should return a user given the user's identification """

    DB.drop_all()
    DB.create_all()

    first_name  = 'Jane'
    last_name   = 'Doe'
    username    = 'jdoe'
    email       = 'jdoe@anonpersons.com'
    password    = 'weakerpass'

    user = User(
        first_name=first_name,
        last_name=last_name,
        username=username,
        email=email,
        password=password
    )

    # Persist the user in the database
    DB.session.add(user)
    DB.session.commit()

    jane = User.query.filter_by(username='jdoe').first()
    assert jane.id is not None
    assert jane.first_name == first_name
    assert jane.last_name == last_name
    assert jane.email == email

    # Attempt to search for an invalid user
    bad_user = User.query.filter_by(username='bad_user').first()
    assert bad_user is None


def test_user_update():
    """ It should update a user's records """
    first_name  = 'John'
    last_name   = 'Smith'
    username    = 'jsmith'
    email       = 'jsmith@anonmail.com'
    password    = 'weakpass'

    user = User(
        first_name=first_name,
        last_name=last_name,
        username=username,
        email=email,
        password=password
    )

    # Persist the user in the database
    DB.session.add(user)
    DB.session.commit()

    retrieved_user = User.query.filter_by(username='jsmith').first()
    retrieved_user.last_name = 'Wayasay'

    # Save updated user back into the database
    DB.session.add(retrieved_user)
    DB.session.commit()

    # Retrieve newly-update user so we can verify the field new field value
    updated_user = User.query.filter_by(username=retrieved_user.username).first()
    assert updated_user.last_name == retrieved_user.last_name

def test_user_deletion():
    """ It should delete a user from the system """

    first_name  = 'John'
    last_name   = 'Smith'
    username    = 'jsmith'
    email       = 'jsmith200@anonmail.com'
    password    = 'weakpass'

    user = User(
        first_name=first_name,
        last_name=last_name,
        username=username,
        email=email,
        password=password
    )

    # Persist the user in the database
    DB.session.add(user)
    DB.session.commit()

    assert User.query.filter_by(username=username).first().username == username
    DB.session.delete(user)
    assert User.query.filter_by(username=username).first().username != username
