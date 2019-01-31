
from madness import Madness, request, context, json, response

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
        yield json.response({'message': exception.message}, status=exception.status)

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
    return response([text], mimetype='text/html')


@app.route
def throw():
    raise APIException('error is thrown', status=418)

@app.error(404)
def my404():
    return response(['not found!!'])

@app.route('relative/path')
def mypath():
    return response(['wow!!'])

@app.route(origin='*', methods=['GET', 'OPTIONS'])
def crossdomain():
    return response(['from anywhere!'])

import module
app.extend(module.app, 'module')


if __name__ == '__main__':
    print(app.routes)
    app.run()
