#!/usr/bin/python3
"""Return a view of all amenities"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def show_amenities(amenity_id=None):
    """Show all states or the state that match with the id"""
    if amenity_id is None:
        amenities = storage.all(Amenity).values()
        json_list = []

        for amenity in amenities:
            json_list.append(amenity.to_dict())

        return jsonify(json_list)

    else:

        amenity = storage.get(Amenity, amenity_id)

        if amenity is None:
            abort(404)

        return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id=None):
    """Delete the element and return a empty dictionary"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        amenity = storage.get(Amenity, amenity_id)
        if amenity is not None:
            storage.delete(amenity)
            storage.save()

        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            dic = {}
            return dic, 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Create a new Amenity"""
    if not request.json:
        abort(400, description="Not a JSON")

    if "name" not in request.get_json().keys():
        abort(400, description="Missing name")

    data = request.get_json()
    obj = Amenity(**data)
    obj.save()

    return jsonify(obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id=None):
    """Update a state"""
    if not request.json:
        abort(400, description="Not a JSON")

    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    data = request.get_json()

    for key, value in data.items():
        if key != "id" or key is not "created_at" or key is not "updated_at":
            setattr(amenity, key, value)

    storage.save()
    return jsonify(amenity.to_dict()), 200
