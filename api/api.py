import base64
import io

import flask
from flask import Flask
from flask_restful import Resource, Api, reqparse
from image_processor import ImageProcessor
from flask_cors import CORS, cross_origin


def decode_image(encoded_image: str) -> io.BytesIO:
    """
    Decodes image data from a request
    :param encoded_image: image data from a request
    :return: decoded PIL image
    """
    image_data = base64.b64decode(encoded_image)
    image = io.BytesIO(image_data)
    return image


class ImageResource(Resource):
    def __init__(self, api):
        self.api = api

    @cross_origin()
    def post(self):
        # import pdb; pdb.set_trace()
        parser = reqparse.RequestParser()
        parser.add_argument('image', type=str, required=True)
        args = parser.parse_args()

        image = args['image']
        decoded_image = decode_image(image)
        verdict = ImageProcessor.process(decoded_image)
        response = flask.jsonify({'verdict': verdict})
        return response


class CleanSurfApi(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = Api(self)

        self.api.add_resource(ImageResource, '/image', resource_class_kwargs={'api': self})

    def run(self, *args, **kwargs):
        super().run(*args, **kwargs)


if __name__ == '__main__':
    app = CleanSurfApi(__name__)
    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.run(debug=True)
