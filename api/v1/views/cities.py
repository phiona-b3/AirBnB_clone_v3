#!/usr/bin/python3
"""Return a view of all cities"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def show_city_at_state(state_id=None):
    """Show all states or the state that match with the id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    cities = state.cities
    json_cities = []
    for city in cities:
        json_cities.append(city.to_dict())

    return jsonify(json_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def show_city(city_id=None):
    """Return a specific state"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id=None):
    """Delete the element and return a empty dictionary"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        city = storage.get(City, city_id)
        if city is not None:
            storage.delete(city)
            storage.save()

        city = storage.get(City, city_id)
        if city is None:
            dic = {}
            return dic, 200


@app_views.route('states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id=None):
    """Create a new City"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    if not request.json:
        abort(400, description="Not a JSON")

    if "name" not in request.get_json().keys():
        abort(400, description="Missing name")

    data = request.get_json()
    obj = City(**data)
    setattr(obj, 'state_id', state_id)
    obj.save()

    return jsonify(obj.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id=None):
    """Update a state"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    if not request.json:
        abort(400, description="Not a JSON")

    data = request.get_json()

    for key, value in data.items():
        if key != "id" or key is not "created_at" or key is not "updated_at":
            setattr(city, key, value)

    storage.save()
    return jsonify(city.to_dict()), 200
