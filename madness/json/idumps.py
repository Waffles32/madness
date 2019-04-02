
from json import dumps
from more_itertools import intersperse, islice_extended
from itertools import chain

class Literal(str):
	"""literal JSON content"""
	pass


def idumps(obj, dumps=dumps):
	"""removes None from objects"""

	if isinstance(obj, dict):
		yield '{'
		yield from islice_extended(
			chain.from_iterable(
				(
					dumps(str(key)),
					':',
					''.join(idumps(value, dumps=dumps)),
					','
				)
				for key, value in obj.items()
				if value != None
			),
			None,
			-1
		)
		yield '}'
		return

	if not isinstance(obj, (str, bytes)):
		try:
			gen = iter(obj)
		except TypeError:
			pass
		else:
			yield '['
			yield from intersperse(',', map(lambda value: ''.join(idumps(value, dumps=dumps)), gen))
			yield ']'
			return

	yield obj if isinstance(obj, Literal) else dumps(obj)


if __name__ == '__main__':
	obj = {'x': 1, 'y': 2, 'z': [4,5,6]}
	gen = idumps(obj)
	gen = list(gen)
	print(gen)
	print('out=',''.join(gen))
