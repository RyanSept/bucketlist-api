import sys
sys.path.append('..')

from app import app
from app.models import User, BucketList, ListItem
from flask_httpauth import HTTPBasicAuth
from flask import request, g, jsonify, abort

auth = HTTPBasicAuth()


@app.route('/auth/login', methods=['POST'])
def login():
    if request.method == 'POST':
        print(request.get_json(), dir(request))
        json = request.get_json()
        if json['email'] is None or json['password'] is None:
            abort(400)  # missing arguments
        auth = verify_password(json['email'], json['password'])
        if auth:
            return jsonify({'username': g.user.first_name + ' ' + g.user.last_name,
                            'email': g.user.email})


@auth.verify_password
def verify_password(email, password):
    g.user = User.query.filter(email==User.email).first()
    return g.user is not None and g.user.check_password(password)
