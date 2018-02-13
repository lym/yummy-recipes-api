from flask import (
    abort,
    jsonify,
    request,
)
from flask_restful import Resource

from models import User


class LoginController(Resource):
    def post(self):
        # Allow either form-encoded or raw JSON strings
        user_credentials = request.get_json() or request.form
        if len(user_credentials) == 0:  # user_credentials dict is empty
            abort(400, 'Please supply email and password')
        email = user_credentials.get('email')
        if email is None:
            abort(400, 'You need to supply an email address attribute')
        passw = user_credentials.get('password')
        if passw is None:
            return {'message': 'You need to supply a password attribute'}, 400
        existant_user = User.query.filter_by(email=email).first()
        if existant_user is None:
            return {
                'message': 'You are not Authorized to access this resource'
            }, 401
        if ((existant_user.email == email) and
                (existant_user.password == passw)):
            token = existant_user.auth_token
            res = {'token': token}
            return jsonify(res)
        return {
            'message': 'You are not Authorized to access this resource'
        }, 401
