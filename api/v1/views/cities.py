#!/usr/bin/python3
"""handles all default RESTFul API actions related to City"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Retrieve the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    # cities = storage.all(City)
    citiess = state.cities
    return jsonify([city.to_dict() for city in citiess])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_a_city(city_id):
    '''Retrieves a City object'''
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_a_city(city_id):
    '''Deletes a City object'''
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def add_city(state_id):
    '''Creates a City'''
    state = storage.get('State', state_id)
    if not state:
        abort(404)  # to update a city drom a state, get the state first
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    #citydict = request.get_json()
    #new_city = City(state_id=state_id, name=citydict['name'])
    new_city = City(**new_city)
    setattr(new_city, 'state_id', state_id)
    storage.new(new_city)
    storage.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    '''Updates a City object'''
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    httpbody = request.get_json()
    for key, value in httpbody.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
