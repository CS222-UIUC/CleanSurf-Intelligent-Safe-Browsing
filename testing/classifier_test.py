# Import modu# Import module
from nudenet import NudeClassifier

# initialize classifier (downloads the checkpoint file automatically the first time)
classifier = NudeClassifier()

# Classify single image
print("For the explicit image", classifier.classify('EXPLICIT/test_image.jpeg'))
print("For the flower", classifier.classify('EXPLICIT/flowers.jpg'))

if (classifier.classify('EXPLICIT/test_image.jpeg')['EXPLICIT/test_image.jpeg']['unsafe'] > 0.5):
    project_class('EXPLICIT/test_image.jpeg').blur_it()
if (classifier.classify('EXPLICIT/flowers.jpg')['EXPLICIT/flowers.jpg']['unsafe'] > 0.5):
    project_class('EXPLICIT/test_image.jpeg').blur_it()

# Returns {'path_to_image_1': {'safe': PROBABILITY, 'unsafe': PROBABILITY}}
# Classify multiple images (batch prediction)
# batch_size is optional; defaults to 4

