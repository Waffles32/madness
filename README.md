# madness

use methods for your madness

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

```console
$ uwsgi --http :9090 --wsgi-file myapp.py --callable=app --master --processes 4 --threads 1
```


## Routing

`@app.route(*paths, methods=[], context=[])`          

option | description
------------ | -------------
`*paths` | relative paths, defaults to the decorated function name
`methods` | list of allowed http methods
`context` | list of extra context functions see [contexts](https://github.com/Waffles32/madness/blob/master/context.md)
`origin` | allowed origin: \* or list of urls
`headers` | allowed request headers: list of header names

***

### convenience methods for `@app.route`

you can still use options with these!

`@app.get, @app.post, @app.put, @app.delete, @app.patch, @app.options`

#### RESTful

these routes bind to specific HTTP method(s) and rewrite the path

decorator | path | method
------------ | ------------- | -------------
`@app.index` | {path} | GET
`@app.new` | new{path} | GET
`@app.create` | {path} | POST
`@app.show` | /:id{path} | GET
`@app.edit` | /:id/edit{path} | GET
`@app.update` | /:id{path} | PATCH/PUT
`@app.destroy` | /:id{path} | DELETE


#### AWS

`@app.lambda_handler`

[usage](https://github.com/Waffles32/madness/blob/development/examples/lambda_handler.py)


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



## Context

madness.context contains the current context

contexts run in the order they are added

[rule args](http://werkzeug.pocoo.org/docs/0.14/routing/) are added to context

e.g. `@app.route('path/<myvar>')` creates `context.myvar`

### A Simple Example

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
