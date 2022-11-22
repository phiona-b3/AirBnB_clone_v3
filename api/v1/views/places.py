#!/usr/bin/python3
"""Return a view of all cities"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def show_place_at_city(city_id=None):
    """Show all cities or the city that match with the id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places = city.places
    json_places = []
    for place in places:
        json_places.append(place.to_dict())

    return jsonify(json_places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def show_place(place_id=None):
    """Return a specific city"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id=None):
    """Delete the element and return a empty dictionary"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        place = storage.get(Place, place_id)
        if place is not None:
            storage.delete(place)
            storage.save()

        place = storage.get(Place, place_id)
        if place is None:
            dic = {}
            return dic, 200


@app_views.route('cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id=None):
    """Create a new place"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    if not request.json:
        abort(400, description="Not a JSON")

    if "user_id" not in request.get_json().keys():
        abort(400, description="Missing user_id")

    if "name" not in request.get_json().keys():
        abort(400, description="Missing name")

    data = request.get_json()

    user = storage.get(User, data["user_id"])
    if user is None:
        abort(404)

    obj = Place(**data)
    setattr(obj, 'city_id', city_id)
    setattr(obj, "user_id", data["user_id"])
    obj.save()

    return jsonify(obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id=None):
    """Update a place"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    if not request.json:
        abort(400, description="Not a JSON")

    data = request.get_json()

    for key, value in data.items():
        if key != "id" or key is not "created_at" or key is not "updated_at":
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200
