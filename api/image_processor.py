import time
import os
import io

from PIL import Image
from nudenet import NudeClassifier

classifier = NudeClassifier()


class ImageProcessor:
    @staticmethod
    def process(image: io.BytesIO) -> dict:
        image_path = 'temp_{}.png'.format(time.time())
        Image.open(image).save(image_path, format='PNG')
        verdict = classifier.classify(image_path)[image_path]
        try:
            os.remove(image_path)
        except OSError:
            print("Could not delete file {}".format(image_path))
        return verdict
    
