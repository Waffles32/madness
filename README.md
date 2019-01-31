# madness

Madness orchestrates the HTTP request-response cycle using context functions to build abstractions and route functions to transform abstractions into a HTTP responses.


## Principles

[DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself)

[Dependency_inversion_principle](https://en.wikipedia.org/wiki/Dependency_inversion_principle)

  use `@context` to build abstractions for your low-level modules `@context and @route`

  e.g.

    @context authenticate the HTTP request `context.username = 'xyz'`

    @context get database connection `context.database = Database()`

    @context(database) select data using the database connection `context.data = database.myobjects.find(context.id)`

    @show(data) convert data to HTTP response `return json.response(data)`

[Do One Thing and Do It Well.](https://en.wikipedia.org/wiki/Unix_philosophy#Do_One_Thing_and_Do_It_Well)


## Installing

```console
$ pip install -U madness
```

## A Simple Example

```python
from madness import Madness, response

app = Madness()

@app.index
def hello():
    return response(['Hello, world!'])

if __name__ == '__main__':
    app.run()
```


## Routing

`@app.route(*paths, methods=[], context=[], origin=None, headers=[])`          

option | description
------------ | -------------
`*paths` | relative paths, defaults to the decorated function name
`methods` | list of allowed http methods
`context` | list of extra context functions see #Context
`origin` | allowed origin: \* or list of urls
`headers` | allowed request headers: list of header names

***

### convenience methods for `@app.route`

you can still use options with these!

`@app.get, @app.post, @app.put, @app.delete, @app.patch, @app.options`

#### RESTful routes

inspired by Ruby on Rails' `resources`

https://gist.github.com/alexpchin/09939db6f81d654af06b

https://medium.com/@shubhangirajagrawal/the-7-restful-routes-a8e84201f206

decorator | path | method
------------ | ------------- | -------------
`@app.index` | {path} | GET
`@app.new` | new{path} | GET
`@app.create` | {path} | POST
`@app.show` | /:id{path} | GET
`@app.edit` | /:id/edit{path} | GET
`@app.update` | /:id{path} | PATCH/PUT
`@app.destroy` | /:id{path} | DELETE


#### AWS Lambda

see also: [RequestResponse](https://docs.aws.amazon.com/lambda/latest/dg/python-programming-model-handler-types.html)

```python
from madness import json

@json.schema
class EventSchema():
    x: int = 1

@app.lambda_handler
def process(event: EventSchema):
    return {'y': event['x'] + 2}
```

if you annotate the event with a marshmallow schema, it is automatically validated :)

### handling routing errors

```python
@app.error(404)
def my404handler():
    return response(['not found'], status = 404)
```

***

## Modules

```python
from madness import Madness, response

app = Madness()

module = Madness()

@module.route
def thing():
    return response(['hello!'])

app.extend(module) # now app has /thing

app.extend(module, 'prefix') # now app has /prefix/thing

app.extend(module, context=False) # add the routes but not the context

if __name__ == '__main__':
  app.run()
```

***

## Context

madness.context contains the current context

contexts run in the order they are added

[rule args](http://werkzeug.pocoo.org/docs/0.14/routing/) are added to context

e.g. `@app.route('path/<myvar>')` creates `context.myvar`


### Basic Context Functions

```python
from madness import context, json

@app.context
def before_request():
    "could do anything here, so let's add a variable to the context!"
    context.x = 2

@app.context
def continue_processing(x):
    "define context.y based on context.x!"
    context.y = x * 3 # 6

@app.route
def double(y):
    "doubles context.y and sends it as a JSON response"
    return json.response(y * 2) # 12

```

***

### Advanced Context Generators

a context has full access to the request/response/exceptions

the response/exception is bubbled through the context handlers

```python
@app.context
def advanced_context():
    # before_request
    if request.headers.get('x-api-key') != 'valid-api-key':
        # abort
        yield json.response({'message': 'invalid api key'}, status = 403)
    else:
        # run remaining context functions and the route endpoint (if not aborted)
        try:
            response = yield

        except MyException as exception:
            yield json.response({'message': exception.message}, status = 500)

        else:
            # modify the response headers
            response.headers['x-added-by-context'] = 'value'

            # abort
            yield json.response('we decided to not send the original response, isn\'t that weird?')

        finally:
            # after_request
            pass

```
