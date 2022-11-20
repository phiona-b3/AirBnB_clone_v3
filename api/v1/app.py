#!/usr/bin/python3
"""starting API"""
from flask import Flask
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(error):
    """method that cals storage.close"""
    storage.close()


if __name == "__main__":
    port_one = '5000'
    host_one = '0.0.0.0'

    if os.getenv('HBNB_API_HOST'):
        host_one = os.getenv('HBNB_API_HOST')

    if os.getenv('HBNB_API_PORT'):
        port_one = os.getenv('HBNB_API_PORT')

    app.run(host=host_one, port=port_one, threaded=True, debug=True)
