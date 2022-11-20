#!/usr/bin/python3
"""starting API"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(error):
    """method that cals storage.close"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Return this if the request not have a match"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    port_one = '5000'
    host_one = '0.0.0.0'

    if os.getenv('HBNB_API_HOST'):
        host_one = os.getenv('HBNB_API_HOST')

    if os.getenv('HBNB_API_PORT'):
        port_one = os.getenv('HBNB_API_PORT')

    app.run(host=host_one, port=port_one, threaded=True, debug=True)
