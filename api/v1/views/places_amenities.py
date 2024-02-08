#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.review import Review
from os import getenv


if getenv('HBNB_TYPE_STORAGE') == 'db':
    @app_views.route('/places/<place_id>/amenities/', methods=['GET'],
                     strict_slashes=False)
    def get_amenities_by_place(place_id):
        """
            amenities route to handle http method for requested amenity/s
        """
        places = storage.all('Place')
        fetch_string = "{}.{}".format('Place', place_id)
        place = places.get(fetch_string)

        if place is None:
            abort(404)

        if request.method == 'GET':
            for place_obj in places:
                if place_obj.id == place_id:
                    amenities = []
                    for amenity in place_obj.amenities:
                        amenities.append(amenity.to_dict())
                    return jsonify(amenities)

    @app_views.route('/places/<place_id>/amenities/<amenity_id>',
                     methods=['POST', 'DELETE'])
    def create_place_amenity(place_id, amenity_id):
        '''Creates a Amenity'''
        places = storage.all('Place')
        place = places.get("Place.{}".format(place_id))

        amenities = storage.all("Amenity")
        amenity = amenities.get("Amenity.{}".format(amenity_id))

        if place is None or amenity is None:
            abort(404)

        if request.method == 'POST':
            amenities = []
            for place_obj in places:
                if place_obj.id == place_id:
                    for amenity_obj in amenities:
                        if amenity_obj.id == amenity_id:
                            place_obj.amenities.append(amenity)
                            storage.save()
                            amenities.append(amenity.to_dict())
                            return jsonify(amenities[0]), 200
            return jsonify(amenities[0]), 201

        if request.method == 'DELETE':
            for place_obj in places:
                if place_obj.id == place_id:
                    for amenity_obj in amenities:
                        if amenity_obj.id == amenity_id:
                            place_obj.amenities.remove(amenity)
                            storage.save()
                            return jsonify({}), 200


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_place_amenity(amenity_id):
    '''Gets a Amenity'''
    amenities = storage.all("Amenity")
    amenity = amenities.get("Amenity.{}".format(amenity_id))

    if amenity is None:
        abort(404)

    return jsonify(amenity.to_dict())
