# Create a test that will send an image to the api and check that the response is correct
from api import CleanSurfApi, encode_image, decode_image, ImageProcessor
from pytest import fixture
from PIL import Image
import requests

SERVER_IP = '127.0.0.1'
SERVER_PORT = 5000

explicit_image_path = '../test_images/test_image.jpeg'
explicit_image = Image.open(explicit_image_path)

non_explicit_image_path = '../test_images/flowers.jpg'
non_explicit_image = Image.open(non_explicit_image_path)


def api_process_explicit_image():
    encoded_image = encode_image(explicit_image)
    response = requests.post('http://{}:{}/image'.format(SERVER_IP, SERVER_PORT), json={"image": encoded_image})
    decoded_image = decode_image(response.json()['image'])
    # save the image
    decoded_image.save('processed_explicit_image.jpeg')


def api_process_non_explicit_image():
    encoded_image = encode_image(non_explicit_image)
    response = requests.post('http://{}:{}/image'.format(SERVER_IP, SERVER_PORT), json={'image': encoded_image})
    decoded_image = decode_image(response.json()['image'])
    # save the image
    decoded_image.save('processed_non_explicit_image.jpeg')


if __name__ == '__main__':
    api_process_explicit_image()
    api_process_non_explicit_image()
