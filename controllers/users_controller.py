import hashlib
from flask import (
    abort,
    request,
    jsonify,
)
from flask.views import MethodView

from models import User
from models.base_model import db as DB
from .base_controller import (
    BaseController,
    UsersEndpoint,
)


class UsersController(MethodView):
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
        if (len(email.split()) == 0 or
                len(password.split()) == 0):
            return jsonify({'status': 400})

        # Check if user already exists
        existant_user = User.query.filter_by(email=email).first()
        if (existant_user is not None) and (existant_user.email == email):
            abort(400, 'User already exists!')

        new_user = User(
            email=email, password=password, first_name=first_name,
            last_name=last_name, username=username, auth_token=token
        )

        DB.session.add(new_user)
        DB.session.commit()
        res = {'status': 201}
        return jsonify(res)

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
