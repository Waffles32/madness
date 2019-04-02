from inspect import isgenerator, getfullargspec
from typing import Iterable, Callable

__all__ = 'run_in_middleware', 'run_in_kwargs'


def run_in_kwargs(kwargs: dict, func: Callable):
	return func(**{
        key: kwargs[key]
        for key in getfullargspec(func).args
    })


def run_in_middleware(func: Callable, middleware: Iterable[Callable]):
    """
    Errors should never pass silently.
    Unless explicitly silenced.
    """

    exitstack = []

    try:
        for func2 in middleware:
            gen = func2()
            if isgenerator(gen):
                try:
                    # context yielded during except handler
                    response = gen.send(None)
                    if response != None:
                        #print(gen, 'except handler returned', response)
                        break
                except StopIteration:
                    pass
                else:
                    exitstack.append(gen)
        else:
            # context did not abort the request
            response = func()

    except Exception as exception:
        # allow context to recover from an error
        current_exception = exception
        response = None
    else:
        current_exception = None

    #print('unstack', repr(current_exception), 'and', response)

    for gen in reversed(exitstack):
        try:
            if current_exception == None:
                new_response = gen.send(response)
            else:
                new_response = gen.throw(current_exception)
        except StopIteration:
            pass
        except Exception as exception:
            current_exception = exception
            response = None
        else:
            if new_response != None:
                current_exception = None
                response = new_response

    if current_exception != None:
        raise current_exception

    return response


if __name__ == '__main__':

    def errorhandler():
        try:
            yield
        except ValueError:
            yield 'there was a ValueError...'

    def a():
        print('a')
        x = yield
        print('x =', x)
        raise ValueError()

    def b():
        print('b')
        c = yield
        yield c + ' (b!)'

    def c():
        print('c')
        return 'C RESULT'


    result = run_in_middleware(c, (errorhandler, a, b))

    print('result is', result)
