#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route('/users/', methods=['GET', 'POST'], strict_slashes=False)
def get_users():
    """
        states route to handle http method for requested state/s
    """

    if request.method == 'GET':
        users = []
        for user in storage.all("User").values():
            users.append(user.to_dict())
        return jsonify(users)

    if request.method == 'POST':
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if 'email' not in request.get_json():
            return make_response(jsonify({'error': 'Missing email'}), 400)
        if 'password' not in request.get_json():
            return make_response(jsonify({'error': 'Missing password'}), 400)
        new_user = User(**request.get_json())
        new_user.save()
        return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_user(user_id):
    """
        states route to handle http methods for requested state
    """
    users = storage.all('User')
    fetch_string = "{}.{}".format('User', user_id)
    user = users.get(fetch_string)
    if user is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(user.to_dict())

    if request.method == 'DELETE':
        user.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for key, value in request.get_json().items():
            if key not in ['id', 'created_at', 'updated_at', 'email']:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict())
