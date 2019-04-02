
from dataclasses import replace

from .routing import routes, route
from .context import request
from .wrappers import response

from typing import List, Any

def options(
    *,
    origin: Any = '*',
    methods: List[str] = [],
    headers: List[str] = [],
    vary: str = None,
    max_age: int = None
):
    methods = methods + ['OPTIONS']
    options_headers = {}
    request_origin = request.environ.get('HTTP_ORIGIN', '*')
    if request_origin in origin:
        options_headers['Access-Control-Allow-Origin'] = request_origin
        options_headers['Access-Control-Allow-Methods'] = ', '.join(methods)
        if headers != None:
            options_headers['Access-Control-Allow-Headers'] = ', '.join(headers)
    if vary:
        options_headers['Vary'] = vary
    if max_age != None:
        options_headers['Access-Control-Max-Age'] = str(max_age)
    return response([], headers=options_headers)

def cors_view(route, **kwargs):
    return lambda : options(methods=route.methods, **kwargs)

def cors(*args, **kwargs):
    """options: origin, methods, headers, vary, max_age"""
    return routes(
        [
            replace(
                route,
                view_func = cors_view(route, **kwargs),
                methods = ['OPTIONS']
            ),
            route
        ]
        for route in routes(*args)
    )
