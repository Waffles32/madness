
from madness import Madness, json

app = Madness()

@json.schema
class MyEvent():
    x: int = 1

@app.lambda_handler
def process(event: MyEvent):
    print('RUN HANDLER')
    # curl -v --data '{"x": []}' 127.0.0.1:9090/process
    # curl --data '{"x": 1}' 127.0.0.1:9090/process
    print('event is', event)
    return {'a': 23}


if __name__ == '__main__':
    app.run()
