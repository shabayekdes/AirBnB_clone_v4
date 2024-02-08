#!/usr/bin/python3
'''Flask server (variable app)'''
from flask import Flask, jsonify, make_response
from models import storage
from os import getenv
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    '''Status of your API'''
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    '''return render_template'''
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
