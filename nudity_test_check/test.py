# Import modu# Import module
from nudenet import NudeClassifier

# initialize classifier (downloads the checkpoint file automatically the first time)
classifier = NudeClassifier()

# Classify single image
print(classifier.classify('EXPLICIT/test_image.jpeg'))
# Returns {'path_to_image_1': {'safe': PROBABILITY, 'unsafe': PROBABILITY}}
# Classify multiple images (batch prediction)
# batch_size is optional; defaults to 4