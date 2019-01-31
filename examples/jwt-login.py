
# https://github.com/jpadilla/pyjwt
# https://stormpath.com/blog/where-to-store-your-jwts-cookies-vs-html5-web-storage
# http://werkzeug.pocoo.org/docs/0.14/contrib/securecookie/

import jwt

from functools import partial

from madness import Madness, json, response, request, context

#from werkzeug.utils import redirect

app = Madness()

@app.context
def jwt_config():
	secret = 'my-secret'
	algorithm = 'HS256'
	class myjwt:
		encode = partial(jwt.encode, key=secret, algorithm=algorithm)
		decode = partial(jwt.decode, key=secret, algorithms=[algorithm])
	context.jwt = myjwt()


@app.post
def login(jwt):
	 # get some data from the json request
	username, password = json.request('username', 'password')

	is_valid = lambda username, password: username and username == password

	if is_valid(username, password):
		token = jwt.encode({'username': username}).decode('utf8')
		response = json.response({'message': 'logged in', 'token': token})
		response.set_cookie('token', token, httponly=True)
		return response
	else:
		return json.response({'message': 'invalid username/password'}, status = 401)


@app.index
def index():
	return response(['''
	<!DOCTYPE html>
		<html>
		<head>
			<script
			  src="https://code.jquery.com/jquery-3.3.1.min.js"
			  integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8="
			  crossorigin="anonymous"></script>

		</head>
		<body>
		<input id='username' type='text' />
		<input id='password' type='password' />
		<button id='submit'>Login</button>

			<script>
			$(document).ready(function() {

				$('#submit').click(function() {

					$.ajax({
					  dataType: "json",
					  url: '/login',
					  method: 'POST',
					  contentType: 'application/json',
					  data: JSON.stringify({
						username: $('#username').val(),
						password: $('#password').val()
					  }),
					  success: function() {
						console.log('done', arguments);
						window.location = '/profile';
					  },
					  error: function(data) {
					  	alert('login error');
					  }
					});

				});
			});
			</script>

		</body>
	</html>
	'''.strip()], mimetype='text/html')



login_required = Madness()

@login_required.context
def jwt_context(jwt):
	encoded = request.cookies.get('token')
	if encoded != None:
		data = jwt.decode(encoded)
		context.username = data['username']
	else:
		yield json.response({'message': 'must be logged in!'}, status = 403)

@login_required.get
def profile(username):
    return response(['welcome back, ', username, '<br /><a href=/logout>logout</a>'], mimetype='text/html')

@login_required.get
def logout(username):
	response = json.response({'message': 'logged out'})
	response.set_cookie('token', '', expires=0, httponly=True)
	response.headers['Location'] = '/'
	response.status_code = 307
	return response

app.extend(login_required)



if __name__ == '__main__':
	app.run()
