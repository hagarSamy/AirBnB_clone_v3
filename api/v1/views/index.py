#!/usr/bin/python3
"""Returns a Json response"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """returns status code"""
    return (jsonify({"status": "OK"}))
