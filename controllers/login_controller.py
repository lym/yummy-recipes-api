from flask import (
    abort,
    jsonify,
    request,
)
from flask.views import MethodView

from models import User


class LoginController(MethodView):
    def post(self):
        if request.get_json() is None:
            abort(400, 'Please supply email and password')
        email = request.get_json().get('email')
        if email is None:
            abort(400, 'You need to supply an email address')
        passw = request.get_json().get('password')
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
