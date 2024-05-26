#!/usr/bin/python3
"""handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieve a list of all State objects"""
    amenities = storage.all(Amenity)
    # added a .values() in for loop
    return jsonify([a.to_dict() for a in amenities.values()])


@app_views.route('/amenities/<amenity_id>',  methods=['GET'],
                 strict_slashes=False)
def get_a_amenities(amenity_id):
    """comment"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_a_amenity(amenity_id):
    """comment"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def add_amenity():
    """comment"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    amenity = Amenity(name=request.get_json()['name'])
    storage.new(amenity)
    storage.save()
    # added a () on to_dict
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',  methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """comment"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    # updating the amenity object's attributes based on the JSON data
    httpbody = request.get_json()
    for key, value in httpbody.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
