from flask import (
    abort,
    jsonify,
    request,
)
from flask.views import MethodView

from models import User


class LoginController(MethodView):
    def post(self):
        # Allow either form-encoded or raw JSON strings
        user_credentials = request.get_json() or request.form
        if user_credentials is None:
            abort(400, 'Please supply email and password')
        email = user_credentials.get('email')
        if email is None:
            abort(400, 'You need to supply an email address')
        passw = user_credentials.get('password')
        if passw is None:
            abort(400, 'You need to supply a password')
        existant_user = User.query.filter_by(email=email).first()
        if existant_user is None:
            abort(401)
        if (existant_user.email == email) and (existant_user.password == passw):
            token = existant_user.auth_token
            res = {'token': token}
            return jsonify(res)
        abort(401)
