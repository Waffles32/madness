
from madness import application, routes, post, json, g

# middleware: abstractions

def lambda_handler():
	g.event: dict = json.request()
	obj = yield
	yield json.response(obj)

def abstract_x(event):
    """abstract the event"""
    g.x: int = event['x']


# views: data transformations, completely abstracted

def add_one(x: int) -> dict:
    return {'x': x + 1}

def subtract_one(x: int) -> dict:
    return {'x': x - 1}


# routes & application: make it accessible via HTTP

app = application(
    routes(
        post(add_one), # POST /api/add_one
        post(subtract_one), # POST /api/subtract_one
        middleware = [lambda_handler, abstract_x],
		path = '/api'
    )
)


if __name__ == '__main__':
    app.run()
