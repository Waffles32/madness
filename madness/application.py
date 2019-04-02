
from dataclasses import replace
from typing import Callable, List

from more_itertools import collapse
from werkzeug.routing import Map
from werkzeug.serving import run_simple
from werkzeug.exceptions import HTTPException
from werkzeug.wrappers import Request

from .routines import run_in_middleware
from .context import local, context, local_manager
from .wrappers import response
from .routing import routes


def force_type_middleware():
	"""...
	similar to Flask's force_type
	allows returning tuple

	body
	body, status
	body, status, headers
	"""
	obj = yield
	if isinstance(obj, (str, bytes)):
		yield response([obj])
	elif isinstance(obj, tuple):
		try:
			body, status, headers = obj
		except ValueError:
			body, status = obj
			headers = {}
		if isinstance(body, (str, bytes)):
			body = [body]
		yield response(body, status=status, headers=headers)


def create_app(*args, middleware: List[Callable] = []) -> Callable:
	"""allows middleware to catch routing errors, returns WSGI application"""
	global Map, local_manager

	url_map = Map([route.as_rule() for route in routes(*args)])

	def get_response(environ, start_response):
		global context
		nonlocal url_map
		urls = url_map.bind_to_environ(environ)
		view_func, kwargs = urls.match()
		context.update(kwargs)
		return view_func()

	def context_middleware(environ, start_response):
		""""""
		global local, HTTPException, Request
		local.request = Request(environ)
		local.context = {}
		try:
			response = yield
		except HTTPException as response:
			yield response

	@local_manager.make_middleware
	def application(environ, start_response):
		global force_type_middleware
		nonlocal middleware, get_response, context_middleware
		response = run_in_middleware(
			lambda : get_response(environ, start_response),
			[
				force_type_middleware,
				lambda : context_middleware(environ, start_response),
				*middleware
			]
		)
		return response(environ, start_response)

	return application


class Application():
	""""""

	def __init__(self, *args, **kwargs):
		super().__init__()
		self.wsgi_app = create_app(*args, **kwargs)

	def __call__(self, environ, start_response):
		return self.wsgi_app(environ, start_response)

	def run(
		self,
		host: str = 'localhost',
		port: int = 9090,
		debug: bool = None,
		use_reloader: bool = None
	):
		run_simple(
			host,
			port,
			self.wsgi_app,
			use_reloader = True if debug == None and use_reloader == None else use_reloader
		)
