#!/usr/bin/python3
"""checking on the status"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """return status ok"""
    return jsonify({"status": "OK"})
