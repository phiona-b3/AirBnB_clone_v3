#!/usr/bin/python3
"""Return a view of all cities"""
from flask import make_response, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def show_reviews_at_place(place_id=None):
    """Show all reviews id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews = place.reviews
    json_reviews = []
    for review in reviews:
        json_reviews.append(review.to_dict())

    return jsonify(json_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def show_review(review_id=None):
    """Return a specific review"""
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id=None):
    """Delete the element and return a empty dictionary"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    if review is not None:
        storage.delete(review)
        storage.save()

    review = storage.get(Review, review_id)
    if review is None:
        dic = {}
        return make_response(jsonify(dic), 200)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id=None):
    """Create a new place"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    if "user_id" not in request.get_json():
        abort(400, description="Missing user_id")

    if "text" not in request.get_json():
        abort(400, description="Missing text")

    data = request.get_json()

    user = storage.get(User, data["user_id"])
    if user is None:
        abort(404)

    data["place_id"] = place_id
    obj = Review(**data)
    obj.save()

    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id=None):
    """Update a review"""
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()

    for key, value in data.items():
        if key not in ["id", "created_at",
                       "updated_at", "user_id", "place_id"]:
            setattr(review, key, value)

    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
