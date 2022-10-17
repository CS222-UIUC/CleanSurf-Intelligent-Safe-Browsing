import base64
import io

from flask import Flask
from flask_restful import Resource, Api, reqparse
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
    image.save(buffered, format="JPEG")
    img_bytes = base64.b64encode(buffered.getvalue())
    return img_bytes.decode('utf-8')


# Temporary class
class ImageProcessor:
    def processor(self, image):
        # return image of same shape but with all pixels set to red
        red_image = image.copy()
        red_image[:, :, 0] = 255
        red_image[:, :, 1] = 0
        red_image[:, :, 2] = 0
        return red_image


class ImageResource(Resource):
    def __init__(self, api):
        self.api = api

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('image', type=str, required=True)
        args = parser.parse_args()

        image = args['image']
        decoded_image = decode_image(image)
        processed_image = self.api.image_processor.processor(decoded_image)
        encoded_image = encode_image(processed_image)

        return {'image': encoded_image}


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
    app.run(debug=True)
