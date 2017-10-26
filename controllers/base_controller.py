from models import (
    User,
    Recipe,
)


RootEndpoint = 'http://127.0.0.1:5000'
UsersEndpoint = RootEndpoint + '/users/'
RecipesEndpoint = RootEndpoint + '/recipes/'
InstructionsEndpoint = RootEndpoint + '/instructions/'
IngredientsEndpoint = RootEndpoint + '/ingredients/'


class BaseController:
    def authorized(req):
        """ Probes a request object's headers for the Authorization value, a
        token. If the token value found belongs to any of our users we accept
        the request, otherwise we reject.

        Note that at this point the protected areas of the API are accessible
        to any of our registered users

        The Authorization header takes the form:
            Authorization: Token <token value>
        """
        auth_value = req.headers.get('Authorization')
        if auth_value is None:  # No Auth header so request is invalid
            return False
        token = auth_value.split(sep=' ')[-1]
        existant_user = User.query.filter_by(auth_token=token).first()
        if existant_user is None:
            return False
        return True

    @classmethod
    def get_auth_token(cls, req):
        auth_value = req.headers.get('Authorization')
        if auth_value is None:
            return None
        auth_token = auth_value.split(sep=' ')[-1]
        return auth_token

    @classmethod
    def authorized_and_owns_recipe(cls, req, recipe_id):
        req_token = cls.get_auth_token(req)
        if req_token is None:
            return False
        recipe = Recipe.query.filter_by(id=recipe_id).first()
        recipe_owner_id = recipe.user_id
        auth_user_token = req_token
        auth_user = User.query.filter_by(auth_token=auth_user_token).first()
        if recipe_owner_id == auth_user.id:
            return True
        return False

    @classmethod
    def auth_user(cls, req):
        auth_token = cls.get_auth_token(req)
        if auth_token is None:
            return None
        auth_user_token = auth_token
        auth_user = User.query.filter_by(auth_token=auth_user_token).first()
        return auth_user
