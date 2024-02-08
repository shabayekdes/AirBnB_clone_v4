#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import City


@app_views.route('/states/<state_id>/cities/', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_cities(state_id):
    """
        cities route to handle http method for requested city/s
    """
    states = storage.all('State')
    fetch_string = "{}.{}".format('State', state_id)
    state = states.get(fetch_string)

    if state is None:
        abort(404)

    if request.method == 'GET':
        cities = []
        for city in state.cities:
            cities.append(city.to_dict())
        return jsonify(cities)

    if request.method == 'POST':
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if 'name' not in request.get_json():
            return make_response(jsonify({'error': 'Missing name'}), 400)
        kwargs = request.get_json()
        kwargs['state_id'] = state_id
        new_city = City(**kwargs)
        new_city.save()
        return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_city(city_id):
    """
        cities route to handle http methods for requested city
    """
    cities = storage.all('City')
    fetch_string = "{}.{}".format('City', city_id)
    city = cities.get(fetch_string)

    if city is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())

    if request.method == 'DELETE':
        city.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for key, value in request.get_json().items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
