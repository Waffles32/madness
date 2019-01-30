
from madness import Madness, Response, request

from exceptions import Forbidden

app = Madness()

def user():
    username = request.headers.get('x-username')
    if username != None:
        context.username = username
    else:
        raise Forbidden()

@app.index
def home(x):
    text = f'''
    <!DOCTYPE html>
    <html>
        <head>
        </head>
        <body>
            <center>
            <h1>Welcome to Module</h1>
            <h2>x is {x}</h2>
            <a href='{request.path}/protected'>protected page</a>
            <a href='module.json'>module info</a>
            <hr>
            <a href='..'>back</a>
            </center>
        </body>
    </html
    '''
    return Response([text], mimetype='text/html')


@app.route('/protected', context=[user])
def greet(username):
    return Response([f'welcome back, {username}'])

@app.route('.json')
def describe():
    return Response(['{"version": "0.0.1"}'], mimetype='application/json; charset=utf-8')
