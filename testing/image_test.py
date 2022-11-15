# Import modu# Import module
from nudenet import NudeClassifier
from nudenet import NudeDetector
from api.image_processor import *

# initialize classifier (downloads the checkpoint file automatically the first time)
classifier = NudeClassifier()
detector = NudeDetector()

# Classify single image
print("For the explicit image", classifier.classify('EXPLICIT/test_image.jpeg'))    # Returns {'path_to_image_1': {'safe': PROBABILITY, 'unsafe': PROBABILITY}}
print("For the flower", classifier.classify('EXPLICIT/flowers.jpg'))    
print("For the explicit image", classifier.classify('EXPLICIT/painting.jpg'))

print("For the explicit image", detector.detect('EXPLICIT/test_image.jpeg'))    # Returns [{'box': LIST_OF_COORDINATES, 'score': PROBABILITY, 'label': LABEL}, ...]
print("For the explicit video", classifier.classify_video('EXPLICIT/explicit_test_video.mp4')) # Returns {"metadata": {"fps": FPS, "video_length": TOTAL_N_FRAMES, "video_path": 'path_to_video'},"preds": {frame_i: {'safe': PROBABILITY, 'unsafe': PROBABILITY}, ....}}

if (classifier.classify('EXPLICIT/test_image.jpeg')['EXPLICIT/test_image.jpeg']['unsafe'] > 0.5):
   ImageProcessor().blur('EXPLICIT/test_image.jpeg')
if (classifier.classify('EXPLICIT/flowers.jpg')['EXPLICIT/flowers.jpg']['unsafe'] > 0.5):
    ImageProcessor().blur('EXPLICIT/flowers.jpg')





