#!/usr/bin/python3
"""Returns a Json response"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """returns status code"""
    return (jsonify({"status": "OK"}))


@app_views.route('/stats')
def no_of_objects():
    """retrieves the number of each objects by type"""
    objects = {
        "amenities": storage.count('Amenity'),
        "cities": storage.count('City'),
        "places": storage.count('Place'),
        "reviews": storage.count('Review'),
        "states": storage.count('State'),
        "users": storage.count('User'),
    }
    return (jsonify(objects))
