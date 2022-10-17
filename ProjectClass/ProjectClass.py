from PIL import Image, ImageFilter


# Opens a image in RGB mode


class project_class:
    def __init__(self, imagename):
        self.imagetoprocess = Image.open(imagename)
    def blur_it(self):
        # Blurring the image
        img = self.imagetoprocess.filter(ImageFilter.GaussianBlur(25))
        # Shows the image in image viewer
        img.show()
    
