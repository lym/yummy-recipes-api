from flask import (
    abort,
    request,
    jsonify,
)
from flask.views import MethodView

from models import User
from .base_controller import BaseController


class UsersShowController(MethodView):
    """ Handles requests for a single user entity """
    def get(self, user_id):
        print('Requested User ID is: {}'.format(user_id))
        if not BaseController.authorized(request):
            abort(401)
        user_id = int(user_id)
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            abort(404)
        record = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'username': user.username,
            'created': user.created,
            'modified': user.modified
        }
        res = jsonify(record)
        return res
