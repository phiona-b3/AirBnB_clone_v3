#!/usr/bin/python3
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def show_amenities(amenity_id=None):
    """retrieves a list of amenity objects"""
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


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenities(amenity_id=None):
    """deletes a amenity object"""
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
    """create a amenities object"""
    if not request.json:
        abort(400, description="Missing name")

    data = request.get_json()
    obj = Amenity(**data)
    obj.save()

    return jsonify(obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id=None):
    """update amenity objects"""
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    if not request.json:
        abort(400, description="Not a JSON")

    data = request.get_json()

    for key, value in data.items():
        if key != "id" or key is not "created_at" or key is not "updated_at":
            setattr(amenity, key, value)

    storage.save()
    return jsonify(amenity.to_dict()), 200
