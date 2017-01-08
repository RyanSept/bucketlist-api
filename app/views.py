import sys
sys.path.append('..')

from app import app, db
from app.models import User, BucketList, ListItem
from flask_jwt import JWT, jwt_required, current_identity
from flask import request, g, jsonify, abort
from app.validate import validate_register, validate_bucketlist


def verify_password(email, password):
    g.user = User.query.filter(email == User.email).first()
    if g.user is not None and g.user.check_password(password):
        return g.user
    return False


def identity(payload):
    user_id = payload['identity']
    return User.query.filter(user_id == User.user_id).first()


jwt = JWT(app, verify_password, identity)


def user_exists(email):
    exists = db.session.query(db.session.query(User)
                              .filter_by(email=email)
                              .exists()).scalar()
    return exists


@app.route("/resource", methods=['POST'])
@jwt_required()
def get_resource():
    return jsonify(dict(msg="Hello world"))


@app.route("/auth/register", methods=['POST'])
def register_user():
    response = {}
    json = request.json
    validation = validate_register(json)
    if validation.status:
        if not user_exists(json["email"]):
            user = User(
                first_name=json["first_name"],
                last_name=json["last_name"],
                email=json["email"],
                password=json["password"]
            )
            db.session.add(user)
            db.session.commit()
            status_code = 201
        else:
            status_code = 409
            response["message"] = \
                "The user with the email %s already exists" % (json["email"])
    else:
        status_code = 400

    response["message"] = validation.message
    response = jsonify(response)
    response.status_code = status_code
    return response


@app.route("/bucketlists", methods=['POST'])
@jwt_required()
def create_bucketlist():
    '''Create a new bucket list'''
    # validate request
    # create bucketlist adding it to the current user's list of bucketlists
    # return response
    response = {}
    json = request.json
    validation = validate_bucketlist(json)
    if validation.status:
        bucketlist = BucketList(name=json['name'])
        current_identity.bucketlists.append(bucketlist)
        db.session.add(bucketlist)
        db.session.commit()
        status_code = 201
    else:
        status_code = 400

    response["message"] = validation.message
    response = jsonify(response)
    response.status_code = status_code
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
