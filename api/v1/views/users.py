#!/usr/bin/python3
"""handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieve a list of all State objects"""
    users = storage.all(User)
    # added a .values() in for loop
    return jsonify([a.to_dict() for a in users.values()])


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_a_user(user_id):
    """comment"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_a_users(user_id):
    """comment"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def add_user():
    """comment"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    # added checks for email and pass
    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")
    user = User(name=request.get_json()['name'])
    storage.new(user)
    storage.save()
    # added a () on to_dict
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """comment"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    # updating the user object's attributes based on the JSON data
    httpbody = request.get_json()
    for key, value in httpbody.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
