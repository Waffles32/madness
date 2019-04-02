
from madness import (
	request, context, json, response,
	application, routes, route, get, post, index,
	abort, NotFound
)

from standard_stream_middleware import capture_output

### MIDDLEWARE ###

def logging():
	try:
		yield
	except NotFound:
		print('interesting...')
		yield 'custom 404 page', 404
	finally:
		print(request.method, request.path, '->', repr(context['output']))


def authenticate():
	print('authenticating...')
	context['username'] = 'guest'

def authorize():
	print('authorizing...')
	if context['username'] == 'foo':
		abort(403)


### VIEWS ###

def login():
	username, password = json.request('username', 'password')
	valid = username == password
	if not valid:
		abort(401)


USERS = {
	1: {'name': 'Waffles32'},
	2: {'name': 'foo'},
	3: {'name': 'bar'}
}

# JSON resource
users = routes(
	index(lambda: USERS),
	get('/<int:user_id>', lambda user_id: USERS.get(user_id) or abort(404)),
	middleware = [json.jsonify]
)

site = routes(
	index(lambda: 'Hello, world!'), # /
	route('/register', lambda: abort(404)),
	post(login), # /login
	routes(
		routes(users, path = '/users', middleware = [authorize]),
		get('/profile', lambda username: f'Welcome, {username}!'),
		middleware = [authenticate],
	)
)

app = application(
	site,
	middleware = [logging, capture_output]
)

if __name__ == '__main__':
	app.run()
