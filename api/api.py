import base64
import io

import flask
from flask import Flask
from flask_restful import Resource, Api, reqparse
from image_processor import ImageProcessor
from flask_cors import CORS, cross_origin
from PIL import Image


def decode_image(encoded_image: str) -> Image:
    """
    Decodes image data from a request
    :param encoded_image: image data from a request
    :return: decoded PIL image
    """
    image_data = base64.b64decode(encoded_image)
    image = Image.open(io.BytesIO(image_data))
    return image


def encode_image(image: Image) -> str:
    """
    Encodes image data to a request
    :param image: image data from a request
    :return: encoded PIL image
    """
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_bytes = base64.b64encode(buffered.getvalue())
    return img_bytes.decode('utf-8')


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
        # print(image)
        decoded_image = decode_image(image)
        processed_image = self.api.image_processor.process(decoded_image)
        encoded_image = encode_image(processed_image)
        response = flask.jsonify({'image': encoded_image})
        # response.headers.add('Access-Control-Allow-Origin', '*')
        return response


class CleanSurfApi(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = Api(self)
        self.image_processor = ImageProcessor()

        self.api.add_resource(ImageResource, '/image', resource_class_kwargs={'api': self})

    def run(self, *args, **kwargs):
        super().run(*args, **kwargs)


if __name__ == '__main__':
    app = CleanSurfApi(__name__)
    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.run(debug=True)
