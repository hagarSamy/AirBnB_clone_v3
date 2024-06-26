#!/usr/bin/python3
"""handles all default RESTFul API actions related to States"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State


@app_views.route('/states',
                 methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieve a list of all State objects"""
    states = storage.all(State)
    return jsonify([state.to_dict() for state in states.values()])


@app_views.route('/states/<state_id>',
                 methods=['GET'], strict_slashes=False)
def get_a_state(state_id):
    """Retrieves a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_a_state(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states',
                 methods=['POST'], strict_slashes=False)
def add_state():
    """Creates a State"""
    # if not request.json:
    try:
        request.get_json()
    except Exception:
        abort(400, description="Not a JSON")
    # if 'name' not in request.json:
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    statedict = request.get_json()
    new_state = State(name=statedict['name'])
    storage.new(new_state)
    storage.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>',
                 methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    # if not request.json:
    try:
        request.get_json()
    except Exception:
        abort(400, description="Not a JSON")
    httpbody = request.json
    for key, value in httpbody.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
