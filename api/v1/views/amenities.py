#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities/', methods=['GET', 'POST'], strict_slashes=False)
def get_amenities():
    """
        states route to handle http method for requested state/s
    """

    if request.method == 'GET':
        amenities = []
        for amenity in storage.all('Amenity').values():
            amenities.append(amenity.to_dict())
        return jsonify(amenities)

    if request.method == 'POST':
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if 'name' not in request.get_json():
            return make_response(jsonify({'error': 'Missing name'}), 400)
        new_amenity = Amenity(**request.get_json())
        new_amenity.save()
        return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """
        states route to handle http methods for requested state
    """
    amenities = storage.all('Amenity')
    fetch_string = "{}.{}".format('Amenity', amenity_id)
    amenity = amenities.get(fetch_string)
    if amenity is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(amenity.to_dict())

    if request.method == 'DELETE':
        amenity.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for key, value in request.get_json().items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict())
