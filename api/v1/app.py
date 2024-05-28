#!/usr/bin/python3
"""creating a flask application"""

import os
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask import jsonify
from flask_cors import CORS


app = Flask(__name__)

app.register_blueprint(app_views)

# initialize CORS with the app instance
# used "*" insteaed of "0.0.0.0" to allow all origins
# -- moved to if __name__ == "__main__"
# CORS(app, resources={r"/*": {"origins": "*"}})


@app.teardown_appcontext
def teardown(exception):
    """closes the current SQLAchemy session"""
    storage.close()


@app.errorhandler(404)
def notfound(error):
    """returns a JSON-formatted 404 status code response"""
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    # make_response(jsonify({"error": "Not found"}), 404)
    return (response)


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.run(host=host, port=port, threaded=True)
