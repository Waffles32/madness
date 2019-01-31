
from madness import Madness, response, request, json

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
    return response([text], mimetype='text/html')


@app.route('/protected', context=[user])
def greet(username):
    return response([f'welcome back, {username}'])

@app.route('.json')
def describe():
    return json.response({"version": "0.0.1"})
