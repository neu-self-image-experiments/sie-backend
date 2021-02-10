from flask import escape
from flask_restful import Resource, Api

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)

# Set this to false when deploying to live application
app.config['DEBUG'] = True

# Allow cross-origin resource sharing
cors = CORS(app, resources={r'/api/*': {'origins': '*'}})


@app.route('/', methods=['GET'])
def testingServer():
    message = 'hello world!'
    return jsonify({'response': message})


def hello_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'name' in request_json:
        name = request_json['name']
    elif request_args and 'name' in request_args:
        name = request_args['name']
    else:
        name = 'World'
    return 'Hello {}!'.format(escape(name))


if __name__ == '__main__':
    # change the port number if 4000 doesn't work on your local machine
    app.run(host='127.0.0.1', port=4000)
