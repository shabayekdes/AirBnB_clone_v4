#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews/', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_reviews(place_id):
    """
        states route to handle http method for requested state/s
    """
    places = storage.all('Place')
    fetch_string = "{}.{}".format('Place', place_id)
    place = places.get(fetch_string)

    if place is None:
        abort(404)

    if request.method == 'GET':
        reviews = []
        for review in place.reviews:
            reviews.append(review.to_dict())
        return jsonify(reviews)

    if request.method == 'POST':
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if 'user_id' not in request.get_json():
            return make_response(jsonify({'error': 'Missing user_id'}), 400)
        if 'text' not in request.get_json():
            return make_response(jsonify({'error': 'Missing text'}), 400)
        kwargs = request.get_json()
        users = storage.all('User')
        fetch_string = "{}.{}".format('User', kwargs['user_id'])
        user = users.get(fetch_string)
        if user is None:
            abort(404)
        kwargs['place_id'] = place_id
        new_review = Review(**kwargs)
        new_review.save()
        return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_review(review_id):
    """
        states route to handle http methods for requested state
    """
    reviews = storage.all('Review')
    fetch_string = "{}.{}".format('Review', review_id)
    review = reviews.get(fetch_string)

    if review is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(review.to_dict())

    if request.method == 'DELETE':
        review.delete()
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        kwargs = request.get_json()
        for key, value in kwargs.items():
            if key not in ['id', 'user_id', 'place_id', 'created_at',
                           'updated_at']:
                setattr(review, key, value)
        review.save()
        return make_response(jsonify(review.to_dict()), 200)
