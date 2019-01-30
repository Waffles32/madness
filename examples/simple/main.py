
from json import dumps

from madness import Madness, Response, request, context

from exceptions import APIException

app = Madness()

@app.context
def setup():
    context.x = 3101

@app.context
def catch():
    """
    render APIException to JSON
    """
    try:
        response = yield
    except APIException as exception:
        text = dumps({'message': exception.message}, indent=True)
        yield Response(
            [text],
            status = exception.status,
            mimetype='application/json; charset=utf-8'
        )

@app.index
def home(x):
    text = f'''
    <!DOCTYPE html>
    <html>
        <head>
        </head>
        <body>
            <center>
            <h1>Welcome to Madness</h1>
            <h2>x is {x}</h2>
            <a href='throw'>raise api exception</a>
            <a href='invalid-route'>404 page</a>
            <a href='relative/path'>relative path!</a>

            <hr>
            <a href='module'>module</a>

            </center>
        </body>
    </html
    '''
    return Response([text], mimetype='text/html')


@app.route
def throw():
    raise APIException('error is thrown', status=418)

@app.error(404)
def my404():
    return Response(['not found!!'])

@app.route('relative/path')
def mypath():
    return Response(['wow!!'])

@app.route(origin='*', methods=['GET', 'OPTIONS'])
def crossdomain():
    return Response(['from anywhere!'])

import module
app.extend(module.app, 'module')



if __name__ == '__main__':
    print(app.routes)
    app.run()
else:
    # WSGI application for production
    application = app.callable()
