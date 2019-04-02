
from madness import application, routes, post, json

# middleware: abstractions

def lambda_handler():
	context['event'] = json.request()
	obj = yield
	yield json.response(obj)

def abstract_x():
    """abstract the event"""
    context['x']: int = context['event']['x']


# views: transformations

def add_one(x: int) -> dict:
    return {'x': x + 1}

def subtract_one(x: int) -> dict:
    return {'x': x - 1}


# routes: make it accessible via HTTP

app = application(
    routes(
        post(add_one),
        post(subtract_one),
        middleware = [lambda_handler, abstract_x]
    )
)


if __name__ == '__main__':
    app.run()
