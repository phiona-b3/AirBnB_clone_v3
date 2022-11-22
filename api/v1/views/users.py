#!/usr/bin/python3
"""Return a view of all users"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def show_users(user_id=None):
    """Show all states or the state that match with the id"""
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


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id=None):
    """Delete the element and return a empty dictionary"""
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
    """Create a new User"""
    if not request.json:
        abort(400, description="Not a JSON")

    if "email" not in request.get_json().keys():
        abort(400, description="Missing email")

    if "password" not in request.get_json().keys():
        abort(400, description="Missing password")

    data = request.get_json()
    obj = User(**data)
    obj.save()

    return jsonify(obj.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_user(user_id=None):
    """Update a state"""
    if not request.json:
        abort(400, description="Not a JSON")

    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    data = request.get_json()

    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at", "email"]:
            setattr(user, key, value)

    storage.save()
    return jsonify(user.to_dict()), 200
