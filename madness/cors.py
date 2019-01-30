
from functools import wraps
from typing import Callable, Tuple, List, Any

from .decorators import decoratormethod

class CORSMixIn():
    "https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS"

    @decoratormethod
    def route(self, endpoint:Callable, *paths:Tuple[str], origin:Any=[], max_age:int=None, vary:str=None, methods:List[str]=[], headers:List[str]=None, **kwargs) -> Callable:
        """
        origin may be a list of urls or '*'
        headers is a whitelist of request headers
        default is to allow all headers
        """

        if 'OPTIONS' in methods:
            @wraps(endpoint)
            def wrapped_endpoint():
                if request.method == 'OPTIONS':

                    options_headers = {}

                    request_origin = request.environ.get('HTTP_ORIGIN', '*')

                    if request_origin in origin:
                        options_headers['Access-Control-Allow-Origin'] = request_origin
                        options_headers['Access-Control-Allow-Methods'] = ', '.join(methods)
                        if 'Access-Control-Request-Headers' in request.headers:
                            if headers == None:
                                allow_headers = request.headers['Access-Control-Request-Headers']
                            else:
                                allow_headers = ', '.join(headers)
                            options_headers['Access-Control-Allow-Headers'] = allow_headers

                    if vary:
                        options_headers['Vary'] = vary

                    if max_age != None:
                        options_headers['Access-Control-Max-Age'] = str(max_age)

                    return Response([], headers=options_headers)
                else:
                    return context.run(endpoint)
        else:
            wrapped_endpoint = endpoint

        super().route(wrapped_endpoint, *paths, methods=methods, **kwargs)
        return endpoint
