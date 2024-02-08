#!/usr/bin/python3
'''api status'''
import models
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', strict_slashes=False)
def ok():
    '''return stuff'''
    return jsonify(status='OK')


@app_views.route('/stats', methods=['GET'])
def stats():
    """
    function to return the count of all class objects
    """
    response = {}
    models = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
    }
    for key, value in models.items():
        response[key] = storage.count(value)
    return jsonify(response)
