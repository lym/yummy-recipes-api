class TestEnv(object):
    """ Test database """
    _db_host       = 'localhost'
    _db_port       = '5432'
    _db_name       = 'yummy_recipes_test'
    _db_user       = 'yr_test_user'
    _db_pass       = 'yr_test_pass'

    DATABASE_URL = "postgres://{}:{}@{}:{}/{}".format(
        _db_user,
        _db_pass,
        _db_host,
        _db_port,
        _db_name
    )

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True


class DevEnv(object):
    """ Test database """
    _db_host       = 'localhost'
    _db_port       = '5432'
    _db_name       = 'yummy_recipes'
    _db_user       = 'yummy_recipes'
    _db_pass       = 'weakpass'

    DATABASE_URL = "postgres://{}:{}@{}:{}/{}".format(
        _db_user,
        _db_pass,
        _db_host,
        _db_port,
        _db_name
    )

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
