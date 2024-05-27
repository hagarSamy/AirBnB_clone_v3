#!/usr/bin/python3
"""handles all default RESTFul API actions related to Place"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.city import City
from models.state import State
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Retrieve the list of all PLace objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = city.places
    # return jsonify([place.to_dict() for place in places.values()])
    return jsonify([place.to_dict() for place in places])


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_a_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_a_place(place_id):
    '''Deletes a Place object:'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def add_place():
    '''Creates a Place'''
    placedict = request.get_json()
    if not placedict:
        abort(400, description="Not a JSON")
    if 'user_id' not in placedict:
        abort(400, description="Missing name")
    user = storage.get(User, placedict['user_id'])
    if 'name' not in placedict:
        abort(400, 'Missing name')
    new_place = Place(**placedict)
    storage.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    '''Updates a Place object'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    httpbody = request.json()
    for key, value in httpbody.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
