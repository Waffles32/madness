

def simple_middleware():
    print('before_request')

def enclosing_middleware():
    print('before_request')
    try:
        response = yield
    finally:
        print('after_request'')

def man_in_the_middleware():
    yield 'this is the new response'

def custom_404_middleware():
    try:
        response = yield
    except NotFound:
        yield 'custom 404 page', 404
