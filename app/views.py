import sys
sys.path.append('..')

from app import app
from app.models import User, BucketList, ListItem
from flask_jwt import JWT, jwt_required, current_identity
from flask import request, g, jsonify, abort


def verify_password(email, password):
    g.user = User.query.filter(email == User.email).first()
    if g.user is not None and g.user.check_password(password):
        return g.user
    return False


def identity(payload):
    user_id = payload['identity']
    return User.query.filter(user_id == User.user_id).first()


jwt = JWT(app, verify_password, identity)


@app.route("/resource", methods=['POST'])
@jwt_required()
def get_resource():
    return jsonify(dict(msg="Hello world"))


@app.route("/auth/register", methods=['POST'])
def register_user():
    pass


@app.route("/bucketlists", methods=['POST'])
@jwt_required()
def create_bucketlist():
    '''Create a new bucket list'''
    response = jsonify({})
    if request.json.get('name'):
        response.status_code = 201
    else:
        response.status_code = 400
    return response

@app.route("/bucketlists", methods=['GET'])
@jwt_required()
def get_all_bucketlists():
    '''List all the created bucket lists'''


@app.route("/bucketlists/<int:bucketlist_id>", methods=['GET'])
@jwt_required()
def get_single_bucketlist():
    pass


@app.route("/bucketlists/<int:bucketlist_id>", methods=['PUT'])
@jwt_required()
def update_single_bucketlist():
    pass


@app.route("/bucketlists/<int:bucketlist_id>", methods=['DELETE'])
@jwt_required()
def delete_single_bucketlist():
    pass


@app.route("/bucketlists/<int:bucketlist_id>/items", methods=['POST'])
@jwt_required()
def create_bucketlist_item():
    pass


@app.route("/bucketlists/<int:id>/items/<int:item_id>", methods=['PUT'])
@jwt_required()
def update_bucketlist_item():
    pass


@app.route("/bucketlists/<int:id>/items/<int:item_id>", methods=['DELETE'])
@jwt_required()
def delete_item_from_bucketlist():
    pass
