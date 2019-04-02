
from madness import route, routes, cors, get, request, response, NotFound, application

api = routes(
    route('/', lambda : 'home'),
    route('/x', lambda: 'slash x'),
    methods = ['GET']
)

staticfiles = get(
    '/<path:filename>',
    lambda filename: f'static content for {filename}'
)

site = routes(
    get('/', lambda: 'hello!'),
    get('/brew', lambda: ('I\'m a teapot!', 418)),
    cors(api, origin = '*', headers = ['x-api-key']),
    cors(
        routes(staticfiles, path = '/static'),
        origin = '*'
    ),
    route('/echo', lambda: request.get_data())
)


def custom404():
    try:
        yield
    except NotFound:
        yield 'Nothing here!', 404

app = application(site, middleware = [custom404])

if __name__ == '__main__':
    app.run(debug=True)
