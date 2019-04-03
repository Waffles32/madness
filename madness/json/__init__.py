

from simplejson import loads, dumps
from functools import partial
from werkzeug.wrappers import Response
from more_itertools import chunked

from ..context import request as _request
from .idumps import idumps

__all__ = 'request', 'response'

def response(obj, bufsize=100000, **kwargs):
	return Response(
		(
			''.join(chunk)
			for chunk in chunked(
				idumps(
					obj,
					dumps = partial(dumps, **kwargs) if kwargs else dumps
				),
				bufsize
			)
		),
		mimetype = 'application/json; charset=utf-8'
	)

def request(*args):
	data = loads(_request.get_data())
	if args:
		return (data[arg] for arg in args)
	return data
