# madness


use methods for your madness

## Application

```python
from madness import Madness

app = Madness()

# add routes/context here

if __name__ == '__main__':
  app.run()
```


## Routing

### Decorators

`@route`          

option | description
------------ | -------------
`*paths` | relative paths
`methods` | list of allowed http methods
`context` | list of extra context functions

#### Single-Method

`@get, @post, @put, @delete, @patch, @options`

#### RESTful

decorator | path | methods
------------ | ------------- | -------------
`@index` | {path} | GET
`@new` | new{path} | GET
`@create` | | POST
`@show` | /<int:id>{path} | GET
`@edit` | /<int:id>/edit{path} | GET
`@update` | /<int:id>{path} | PUT
`@destroy` | /<int:id>{path} | DELETE

#### AWS

`@lambda_handler`

[usage](https://github.com/Waffles32/madness/blob/development/examples/api-gateway.py)

#### CORS

if 'OPTIONS' is present in methods the following options are used

option | description
------------ | -------------
`origin` | allowed origin: \* or list of urls
`headers` | allowed request headers: list of header names


### Modules

```python

app = Madness()

module = Madness()

@module.route
def thing():
  return response(['hello!'])

app.extend(module) # now app has /thing

app.extend(module, 'prefix') # now app has /prefix/thing

app.extend(module, context:bool=True) # choose if module inherits entire app.context

```


## Context

rules are added to context e.g. /path/<myvar> creates context.myvar


```python


from madness import context, request, json

@app.context
def before_request():
    # add a variable to the context
    context.x = 1

@app.context
def uses_x(x):
    print('a previous context defined', x)


@app.context
def around_request():
    # before_request
    try:
      yield
    finally:
      # after_request
      pass


@app.context
def handle_exception():
  try:
    response = yield
  except MyException as exception:
    # MyException error occured while generating the response

    # we can do one of 3 things with it:

    # ignore the exception, continue processing the request
    pass

    # re-raise the exception to the parent context
    raise

    # convert the exception to a response
    yield json.response({'foo': exception.bar})


@app.context
def filter_request():
  # abort the request before the route, route is never called
  if request.headers['x-header'] != 'some-value':
    yield json.response('aborted')


@app.context
def jwt():
    encoded = request.headers['x-jwt']
    data = jwt.decode(encoded)
    context.username = data['username']
    try:
      yield
    else:
      response.headers['x-jwt'] = jwt.encode({
        'username': context.username
      })


@app.route
def test(x, username):
    print('x is', 1)
    print('jwt is', username)
    return response(['body'])


```
