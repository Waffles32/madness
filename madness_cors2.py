
from dataclasses import replace
from typing import List, Any


from madness import routes, route, request, response

def automatic_options(
    route,
    *,
    origin: Any = '*',
    methods: List[str] = [],
    headers: List[str] = None,
    vary: str = None,
    max_age: int = None # '21600'
):

    route2 = route.add_methods(['OPTIONS'])
    allow_methods = ', '.join(route2.methods)
    allow_headers = ', '.join(map(str.upper, headers))

    cors_headers = {
        'Access-Control-Allow-Methods': allow_methods,
        'Access-Control-Allow-Origin': '*',
        'Allow': allow_methods,
    }

    if headers != None:
        cors_headers['Access-Control-Allow-Headers'] = allow_headers

    if max_age != None:
        cors_headers['Access-Control-Max-Age'] = str(max_age)


    def middleware():
        response = yield
        print('adding CORS', response, type(response))
        for key, value in cors_headers.items():
            response.headers[key] = value

    yield replace(
        route,
        view_func = lambda: response([], headers=cors_headers),
        methods = ['OPTIONS'],
        middleware = []
    )
    yield route.insert_middleware([middleware])

def cors(*args, **kwargs):
    """options: origin, methods, headers, vary, max_age"""
    return routes(
        automatic_options(route, **kwargs)
        for route in routes(*args)
    )
