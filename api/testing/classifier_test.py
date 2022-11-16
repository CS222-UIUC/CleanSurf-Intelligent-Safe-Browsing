# Import modu# Import module
from nudenet import NudeClassifier

# initialize classifier (downloads the checkpoint file automatically the first time)
classifier = NudeClassifier()

# Classify single image
print("For the explicit image", classifier.classify('test_images/test_image.jpeg'))
print("For the flower", classifier.classify('test_images/flowers.jpg'))

if (classifier.classify('test_images/test_image.jpeg')['test_images/test_image.jpeg']['unsafe'] > 0.5):
    project_class('test_images/test_image.jpeg').blur_it()
if (classifier.classify('test_images/flowers.jpg')['test_images/flowers.jpg']['unsafe'] > 0.5):
    project_class('test_images/test_image.jpeg').blur_it()

# Returns {'path_to_image_1': {'safe': PROBABILITY, 'unsafe': PROBABILITY}}
# Classify multiple images (batch prediction)
# batch_size is optional; defaults to 4

