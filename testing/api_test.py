import requests
from PIL import Image

from api import encode_image, decode_image
import pytest

SERVER_IP = '127.0.0.1'
SERVER_PORT = 5000


@pytest.fixture
def image():
    image_path = '../EXPLICIT/test_image.jpeg'
    image = Image.open(image_path)
    return image


def test_api(image):
    encoded_image = encode_image(image).replace('/', '-')
    response = requests.get('http://{}:{}/image/{}'.format(SERVER_IP, SERVER_PORT, encoded_image))
    assert response.status_code == 200
    decoded_image = decode_image(response.json()['image'])
    assert decoded_image

    # save decoded image
    print(decoded_image)
    print("Saving image")
    decoded_image.save('decoded_image.jpeg')
