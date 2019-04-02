# https://bottlepy.org/docs/0.12/recipes.html

from madness import application, routes, route, request
from beaker.middleware import SessionMiddleware
from werkzeug.serving import run_simple

def test():
    s = request.environ.get('beaker.session')
    s['test'] = s.get('test', 0) + 1
    s.save()
    return 'Test counter: %d' % s['test']

application = SessionMiddleware(
    application(
        route(test), # /test
    ),
    {
        'session.type': 'file',
        'session.cookie_expires': 300,
        'session.data_dir': './data',
        'session.auto': True
    }
)

if __name__ == '__main__':
    run_simple('localhost', 9090, application, use_reloader=True)
