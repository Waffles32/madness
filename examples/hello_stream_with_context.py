#!/usr/bin/env python3.7

from io import StringIO
from contextlib import redirect_stdout, redirect_stderr

from madness import application, index, request, response


def logging_middleware():
	"""
	captures output while handling a request (even if there's not a route)
	up until the final byte is sent
	"""
	stream = StringIO()
	try:
		with redirect_stderr(stream):
			with redirect_stdout(stream):
				print(request.method, request.path)
				print(request.headers)
				response = yield
				print(response)
				print(response.headers)
				# wait for response to send before ending the log stream
				yield
	finally:
		print('<REQUEST-LOG>')
		print(stream.getvalue())
		print('</REQUEST-LOG>')


def view_func():
	def generate():
		print('generating response...')
		yield 'a'
		print('another print')
		yield 'b'
	return response(generate())


app = application(
    index(view_func),
    middleware = [logging_middleware]
)

if __name__ == '__main__':
	app.run()
