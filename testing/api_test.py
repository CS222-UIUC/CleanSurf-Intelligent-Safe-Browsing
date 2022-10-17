# Create a test that will send an image to the api and check that the response is correct
from api.api import CleanSurfApi, encode_image, decode_image, ImageProcessor
from pytest import fixture
from PIL import Image
import requests

SERVER_IP = '127.0.0.1'
SERVER_PORT = 5000

image_path = '../EXPLICIT/test_image.jpeg'
image = Image.open(image_path)


@fixture
def api_process_image():
    api = CleanSurfApi(__name__)
    api.run(debug=True)

    # Send image to api

    encoded_image = encode_image(image)
    response = requests.post('http://{}:{}/image'.format(SERVER_IP, SERVER_PORT), json={'image': encoded_image})
    decoded_image = decode_image(response.json()['image'])

    return {'success': response.status_code == 200, 'image': decoded_image}


def test_api_process_image(api_process_image):
    processed_image = ImageProcessor().processor(image)
    assert api_process_image['success'] and api_process_image['image'] == processed_image
