from flask import (
    abort,
    request,
    jsonify,
)
from flask.views import MethodView

from fuzzywuzzy import process

from models import User
from .base_controller import BaseController


class UserSearchController(MethodView):
    """ Handles requests for a single user entity """
    def get(self):
        searched_query = request.args.get('q')
        if not BaseController.authorized(request):
            abort(401)

        # Run fuzzy search, Consider 50% good enough
        matched_users = []
        registered_users = User.query.all()
        for user in registered_users:
            choices = [
                user.first_name + ' ' + user.last_name + ' ' + user.username
            ]
            results = process.extract(searched_query, choices)
            if results is []:  # No matches found
                res = []
                return jsonify(res)
            for result in results:
                if result[1] > 50:
                    matched_users.append(user)
        content = []
        for matched_user in matched_users:
            record = {
                'id': matched_user.id,
                'first_name': matched_user.first_name,
                'last_name': matched_user.last_name,
                'email': matched_user.email,
                'username': matched_user.username,
                'created': matched_user.created,
                'modified': matched_user.modified
            }
            content.append(record)
        return jsonify(content)
