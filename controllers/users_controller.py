from flask import (
    abort,
    request,
    jsonify,
)
from flask.views import MethodView
# from flask_api import status

from models import User
from models.base_model import db as DB


class UsersController(MethodView):
    """ Controller for the user resource """
    def post(self):
        """ User registration """
        first_name = request.get_json().get('first_name')
        last_name = request.get_json().get('last_name')
        username = request.get_json().get('username')
        email   = request.get_json().get('email')
        password = request.get_json().get('password')
        # Check for required fields
        if (len(email.split()) == 0 or
                len(password.split()) == 0):
            # abort(status.HTTP_400_BAD_REQUEST)
            return jsonify({'status': 400})

        # Check if user already exists
        existant_user = User.query.filter_by(email=email).first()
        if (existant_user is not None) and (existant_user.email == email):
            print('User already exists!')
            res = jsonify({'status': 400})
            abort(res)

        new_user = User(email=email, password=password, first_name=first_name,
                        last_name=last_name, username=username)

        DB.session.add(new_user)
        DB.session.commit()
        res = {'status': 201}
        return jsonify(res)

    def get(self):
        users = User.query.all()
        content = []
        for user in users:
            record = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'username': user.username
            }
            content.append(record)
        res = jsonify(content)
        # users = jsonify(User.all())
        return res
