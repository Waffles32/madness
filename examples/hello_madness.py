
from madness import (
	request, g, json, response,
	application, routes, route, get, post, index,
	abort, NotFound, cors
)

from hello_stream_with_context import logging_middleware
from hello_routing import custom404

### MIDDLEWARE ###

def authenticate():
	print('authenticating...')
	g.username = 'guest'

def authorize():
	print('authorizing...')
	if g.username == 'foo':
		abort(403)

def jsonify():
	obj = yield
	yield json.response(obj)


### VIEWS ###

def login():
	username, password = json.request('username', 'password')
	valid = username == password
	if not valid:
		abort(401)


# RESTful users routes

USERS = {
	1: {'name': 'Waffles32'},
	2: {'name': 'foo'},
	3: {'name': 'bar'}
}

users = routes(
	index(lambda: USERS),
	get('/<int:user_id>', lambda user_id: USERS.get(user_id) or abort(404)),
	middleware = [jsonify]
)


# put it all together

site = routes(
	index(lambda: 'Hello, world!'), # /
	route('/register', lambda: abort(404)),
	post(login), # /login
	routes(
		routes(users, path = '/users', middleware = [authorize]),
		get('/profile', lambda username: f'Welcome, {username}!'),
		cors(
			get('/example', lambda: 'CORS is enabled!'),
			origin = '*'
		),
		middleware = [authenticate],
	)
)

app = application(
	site,
	middleware = [logging_middleware]
)

if __name__ == '__main__':
	app.run()
