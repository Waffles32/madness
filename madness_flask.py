
def force_type_middleware():
	"""allows returning tuple / str
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


def jsonify():
    pass

request.get_json

def flask():

    intersperse(force_type, routes)

    request_class = FlaskRequest
