
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr

from madness import context

def capture_stdout():
	stdout = StringIO()
	try:
		with redirect_stdout(stdout):
			yield
	finally:
		context['stdout'] = stdout.getvalue()

def capture_stderr():
	stderr = StringIO()
	try:
		with redirect_stderr(stderr):
			yield
	finally:
		context['stderr'] = stderr.getvalue()

def capture_output():
	stream = StringIO()
	try:
		with redirect_stderr(stream):
			with redirect_stdout(stream):
				yield
	finally:
		context['output'] = stream.getvalue()
