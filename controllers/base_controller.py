from models import User


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

    def get_auth_token(req):
        auth_value = req.headers.get('Authorization')
        if auth_value is None:
            return None
        auth_token = auth_value.split(sep=' ')[-1]
        return auth_token
