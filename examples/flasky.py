#!/usr/bin/env python3.7

import sys
sys.path.insert(0, '..')

#from functools import wraps

from madness import Madness, json
from madness.decorators import decoratormethod
from flask import Flask, jsonify


class WSGIRoutingMixIn():
    "allows routing to WSGI applications"

    @decoratormethod
    def error(self, endpoint, status_code, wsgi=False):
        if wsgi:
            wrapped_endpoint = lambda : endpoint

            # @wraps(endpoint)
            # def wrapped_endpoint():
            #     def proxy_application(environ, start_response):
            #         nonlocal endpoint
            #         return endpoint(environ, start_response)
            #     return proxy_application
        else:
            wrapped_endpoint = endpoint
        super().error(status_code)(wrapped_endpoint)
        return endpoint

    @decoratormethod
    def route(self, endpoint, *args, wsgi=False, **kwargs):
        if wsgi:
            for path in args:
                self._mount(endpoint, path)
        else:
            super().route(*args, **kwargs)(endpoint)
        return endpoint


    def _mount(self, application, path):
        @self.route(path, path + '/<path:mount>')
        @wraps(application)
        def application_endpoint():
            def proxy_response(environ, start_response):
                environ['PATH_INFO'] = environ['PATH_INFO'].replace(f'/{path}', '/', 1)
                return application(environ, start_response)
            return proxy_response
        return application



if __name__ == '__main__':

    class ExtendedMadness(WSGIRoutingMixIn, Madness):
        pass


    app = ExtendedMadness()

    @app.index
    def index():
        return json.response({'madness': True}, status=200)


    flask = Flask(__name__)
    flask.debug = True

    @flask.route('/')
    def flask_index():
        return jsonify(index=1)

    @flask.route('/flask')
    def flask_extra():
        response = jsonify(x=22)
        response.status_code = 200
        return response

    # use flask as 404 handler
    app.error(404, wsgi=True)(flask)

    app.route('flaskapp', wsgi=True)(flask)


    if __name__ == '__main__':
        app.run(debug=True)
