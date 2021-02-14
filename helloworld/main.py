import os
import io
from flask import escape, request
from flask_restful import Resource, Api
from google.cloud import vision

from flask import Flask, jsonify
from flask_cors import CORS

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'GVServiceAccountToken.json'

app = Flask(__name__)
api = Api(app)

# Set this to false when deploying to live application
app.config['DEBUG'] = True

# Allow cross-origin resource sharing
cors = CORS(app, resources={r'/api/*': {'origins': '*'}})


def face_detection(uri):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    # _json = request.json
    # _uri = _json['uri']
    # print(_uri)
    vision_client = vision.ImageAnnotatorClient()
    print(vision_client)

    # image = vision.types.Image()
    image = vision.Image()
    image.source.image_uri = uri

    response = vision_client.face_detection(image=image)
    faceAnnotations = response.face_annotations

    likelihood = ('unknown', 'Very unlikely', 'Unlikely',
                  'Possibly', 'Likely', 'Very likely')

    for face in faceAnnotations:
        print('Detection Confidence:  {0}'.format(face.detection_confidence))
        print('Angry likelyhood:  {0}'.format(
            likelihood[face.anger_likelihood]))
        print('Joy likelyhood:  {0}'.format(likelihood[face.joy_likelihood]))
        print('Sorrow likelyhood:  {0}'.format(
            likelihood[face.sorrow_likelihood]))
        print('Surprise likelyhood:  {0}'.format(
            likelihood[face.surprise_likelihood]))
        print('Headwear likelyhood:  {0}'.format(
            likelihood[face.headwear_likelihood]))


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
