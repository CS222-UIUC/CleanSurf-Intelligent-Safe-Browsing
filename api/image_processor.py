import time
import os

from PIL import Image, ImageFilter
from nudenet import NudeClassifier

classifier = NudeClassifier()


class ImageProcessor:
    def __init__(self, threshold: float = 0.5):
        self.threshold = threshold

    def process(self, image: Image) -> Image:
        # Blurring the image
        image_path = 'temp_{}.png'.format(time.time())
        image.save(image_path)
        if classifier.classify(image_path)[image_path]['unsafe'] > self.threshold:
            print("Found explicit content")
            processed_image = image.filter(ImageFilter.GaussianBlur(radius=10))
        else:
            processed_image = image
        try:
            os.remove(image_path)
        except OSError:
            print("Could not delete file {}".format(image_path))
        return processed_image
