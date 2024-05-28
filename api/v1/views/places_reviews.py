#!/usr/bin/python3
"""handles all default RESTFul API actions related to Place-Reviews"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """Retrieve the list of all PLace objects of a City"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = storage.all(Review)
    return jsonify([review.to_dict() for review in reviews.values()])


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_a_review(review_id):
    '''Retrieves a Review object'''
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_a_review(review_id):
    '''Deletes a Review object'''
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def add_review(place_id):
    '''Creates a Review'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    reviewdict = request.get_json()
    if not storage.get(User, reviewdict['user_id']):
            abort(404)
    if 'text' not in reviewdict:
            abort(400, 'Missing text')
    new_review = Place(**reviewdict)
    storage.new(new_review)
    storage.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    '''Updates a Review objec'''
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    httpbody = request.get_json()
    for key, value in httpbody.items():
        if key not in ['id', 'created_at',
                       'user_id', 'place_id', 'updated_at']:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict())
