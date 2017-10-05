import uuid
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
        if (existant_user.email == email) and (existant_user.password == passw):
            # FIXME: This will be the users token property
            token = int(uuid.uuid4())
            res = {'token': token}
            return jsonify(res)

        print('Email: {}\nPass: {}'.format(email, passw))
        abort(401)
