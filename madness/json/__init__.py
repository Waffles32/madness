

from simplejson import loads, dumps
from functools import partial
from werkzeug.wrappers import Response

from ..context import request as _request
from .idumps import idumps

__all__ = 'request', 'response', 'jsonify'

def response(obj, **kwargs):
	return Response(
		idumps(
			obj,
			dumps = partial(dumps, iterable_as_array=True, default=str, use_decimal=True)
		),
		mimetype = 'application/json; charset=utf-8',
		**kwargs
	)

def request(*args):
	data = loads(_request.get_data())
	if args:
		return (data[arg] for arg in args)
	return data

def jsonify():
	"""middleware which converts the response data into JSON"""
	obj = yield
	yield response(obj)
