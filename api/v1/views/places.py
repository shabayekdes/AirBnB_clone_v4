#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places/', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_places(city_id):
    """
        states route to handle http method for requested state/s
    """
    cities = storage.all('City')
    fetch_string = "{}.{}".format('City', city_id)
    city = cities.get(fetch_string)

    if city is None:
        abort(404)

    if request.method == 'GET':
        places = []
        for place in city.places:
            places.append(place.to_dict())
        return jsonify(places)

    if request.method == 'POST':
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if 'user_id' not in request.get_json():
            return make_response(jsonify({'error': 'Missing user_id'}), 400)
        if 'name' not in request.get_json():
            return make_response(jsonify({'error': 'Missing name'}), 400)
        kwargs = request.get_json()
        users = storage.all('User')
        fetch_string = "{}.{}".format('User', kwargs['user_id'])
        user = users.get(fetch_string)
        if user is None:
            abort(404)
        kwargs['city_id'] = city_id
        new_place = Place(**kwargs)
        new_place.save()
        return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_place(place_id):
    """
        states route to handle http methods for requested state
    """
    places = storage.all('Place')
    fetch_string = "{}.{}".format('Place', place_id)
    place = places.get(fetch_string)

    if place is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict())

    if request.method == 'DELETE':
        place.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for key, value in request.get_json().items():
            if key not in ['id', 'created_at', 'updated_at',
                           'user_id', 'city_id']:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict())
