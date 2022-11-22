#!/usr/bin/python3
"""Return a view of all states"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def show_states(state_id=None):
    """Show all states or the state that match with the id"""
    if state_id is None:
        states = storage.all(State).values()
        json_list = []

        for state in states:
            json_list.append(state.to_dict())

        return jsonify(json_list)

    else:

        state = storage.get(State, state_id)

        if state is None:
            abort(404)

        return jsonify(state.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_states(state_id=None):
    """Delete the element and return a empty dictionary"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        state = storage.get(State, state_id)
        if state is not None:
            storage.delete(state)
            storage.save()

        state = storage.get(State, state_id)
        if state is None:
            dic = {}
            return dic, 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Create a new State"""
    if not request.json:
        abort(400, description="Not a JSON")

    if "name" not in request.get_json().keys():
        abort(400, description="Missing name")

    data = request.get_json()
    obj = State(**data)
    obj.save()

    return jsonify(obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id=None):
    """Update a state"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    if not request.json:
        abort(400, description="Not a JSON")

    data = request.get_json()

    for key, value in data.items():
        if key != "id" or key is not "created_at" or key is not "updated_at":
            setattr(state, key, value)

    storage.save()
    return jsonify(state.to_dict()), 200
