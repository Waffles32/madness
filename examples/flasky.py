#!/usr/bin/env python3.7

import sys
sys.path.insert(0, '..')

from madness import Madness, json

from flask import Flask, jsonify

app = Madness()

@app.index
def index():
    return json.response({'madness': True}, status=200)

flask = Flask(__name__)
flask.debug = True

@flask.route('/flask')
def flask_extra():
    response = jsonify(flask=True)
    response.status_code = 200
    return response

@flask.errorhandler(404)
def flask404(e):
    return jsonify(flask404=True)

# use flask routes as fallback
app.error(404, wsgi=True)(flask)

# route /flaskapp to flask's /
app.route('flaskapp', wsgi=True)(flask)


if __name__ == '__main__':
    # curl 127.0.0.1:9090
    # curl 127.0.0.1:9090/flask/
    # curl 127.0.0.1:9090/flaskapp/flask
    # curl 127.0.0.1:9090/invalid-path
    app.run()
