import hashlib
from flask import (
    abort,
    request,
    jsonify,
)
from flask_restful import Resource

from models import User
from .base_controller import (
    BaseController,
    UsersEndpoint,
)


class UsersController(Resource):
    """ Controller for the user resource """

    def _make_token(self, email):
        bytes_token = email.encode()
        message = hashlib.sha256()
        message.update(bytes_token)
        token = message.hexdigest()[0:40]
        return token

    def _make_self_link(self, user):
        link = UsersEndpoint + str(user.id) + '/'
        return link

    def post(self):
        """ User registration """
        if request.get_json() is None:
            abort(400, 'Please supply user credentials as JSON')
        first_name = request.get_json().get('first_name')
        last_name = request.get_json().get('last_name')
        username = request.get_json().get('username')
        email   = request.get_json().get('email')
        password = request.get_json().get('password')
        token = self._make_token(email)
        # Check for required fields
        if (password is None or len(email.split()) == 0 or
                len(password.split()) == 0):
            return {'message': 'Please enter password'}, 400

        # Check if user already exists
        existant_user = User.query.filter_by(email=email).first()
        if (existant_user is not None) and (existant_user.email == email):
            abort(400, 'User already exists!')

        new_user = User(
            email=email, password=password, first_name=first_name,
            last_name=last_name, username=username, auth_token=token
        )

        new_user.save()
        created_user = User.query.filter_by(email=email).first()
        record = {
            'id': created_user.id,
            'first_name': created_user.first_name,
            'last_name': created_user.last_name,
            'email': created_user.email,
            'username': created_user.username,
            'created': created_user.created.strftime('%Y-%m-%d %H:%M:%S'),
            'links': {
                'self': self._make_self_link(created_user)
            }
        }
        return record, 201

    def get(self):
        if not BaseController.authorized(request):
            abort(401, 'Please provide valid user token')
        result_count = request.args.get('limit')
        if result_count is None:
            users = User.query.all()
            content = []
            for user in users:
                record = {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'username': user.username,
                    'links': {
                        'self': self._make_self_link(user)
                    }

                }
                content.append(record)
            res = jsonify(content)
            return res
        users = User.query.limit(int(result_count)).all()
        content = []
        for user in users:
            record = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'username': user.username,
                'links': {
                    'self': self._make_self_link(user)
                }
            }
            content.append(record)
        res = jsonify(content)
        return res
