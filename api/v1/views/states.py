#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET', 'POST'], strict_slashes=False)
def get_states():
    """
        states route to handle http method for requested state/s
    """
    states = storage.all('State')

    if request.method == 'GET':
        states = []
        for state in storage.all("State").values():
            states.append(state.to_dict())
        return jsonify(states)

    if request.method == 'POST':
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if 'name' not in request.get_json():
            return make_response(jsonify({'error': 'Missing name'}), 400)
        new_state = State(**request.get_json())
        new_state.save()
        return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_state(state_id):
    """
        states route to handle http methods for requested state
    """
    states = storage.all('State')
    fetch_string = "{}.{}".format('State', state_id)
    state = states.get(fetch_string)

    if state is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(state.to_dict())

    if request.method == 'DELETE':
        state.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for key, value in request.get_json().items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
