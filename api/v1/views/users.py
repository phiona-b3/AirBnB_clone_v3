#!/usr/bin/python3
"""users.py edit"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def show_users(user_id=None):
    """retrieves a list of user objects"""
    if user_id is None:
        users = storage.all(User).values()
        json_list = []

        for user in users:
            json_list.append(user.to_dict())

            return jsonify(json_list)

    else:
        user = storage.get(User, user_id)
        if user is None:
            abort(404)

        return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_users(user_id=None):
    """deletes a user object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        user = storage.get(User, user_id)
        if user is not None:
            storage.delete(user)
            storage.save()

        user = storage.get(User, user_id)
        if user is None:
            dic = {}
            return dic, 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """create a users object"""
    if not request.json:
        abort(400, description="Not a JSON")
    
    if "email" not in request.get_json().keys():
        abort(400, desciption="Missing email")
    
    if "password" not in request.get_json().keys():
        abort(400, description="Missing password")

    data = request.get_json()
    obj = User(**data)
    obj.save()

    return jsonify(obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id=None):
    """update user objects"""
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    if not request.json:
        abort(400, description="Not a JSON")

    data = request.get_json()

    for key, value in data.items():
        if key != "id" or key != "created_at" or key != "updated_at":
            setattr(user, key, value)

    storage.save()
    return jsonify(user.to_dict()), 200
