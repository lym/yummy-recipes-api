from flask import (
    abort,
    jsonify,
    request,
)
from flask.views import MethodView

from models import User


class LoginController(MethodView):
    def post(self):
        email = request.get_json().get('email')
        passw = request.get_json().get('password')
        existant_user = User.query.filter_by(email=email).first()
        if existant_user is None:
            abort(401)
        if (existant_user.email == email) and (existant_user.password == passw):
            token = existant_user.auth_token
            res = {'token': token}
            return jsonify(res)
        abort(401)
