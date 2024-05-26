#!/usr/bin/python3
"""handles all default RESTFul API actions related to Place"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.city import City
from models.state import State
from models.place import Place


@app_views.route('/cities/<city_id>/places',  methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Retrieve the list of all PLace objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = storage.all(Place)
    return jsonify([place.to_dict() for place in places.values()])


@app_views.route('/places/<place_id>',  methods=['GET'], strict_slashes=False)
def get_a_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',  methods=['DELETE'], strict_slashes=False)
def del_a_place(city_id):
    '''Deletes a Place object:'''
    place = storage.get(Place, city_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places',  methods=['POST'], strict_slashes=False)
def add_place():
    '''Creates a Place'''
    if not request.json:
        abort(400, description="Not a JSON")
    if 'name' not in request.json:
        abort(400, description="Missing name")
    placedict = request.get_json
    new_place = Place(name=placedict['name'])
    storage.new(new_place)
    storage.save()
    return make_response(jsonify(new_place.to_dict()), 201)

@app_views.route('/places/<place_id>',  methods=['PUT'], strict_slashes=False)
def update_place(city_id):
    '''Updates a Place object'''
    place = storage.get(Place, city_id)
    if place is None:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    httpbody = request.get_json()
    for key, value in httpbody.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict())
