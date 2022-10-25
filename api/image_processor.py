from PIL import Image, ImageFilter


class ImageProcessor:
    @staticmethod
    def blur(image: Image) -> Image:
        # Blurring the image
        Image.open(image).filter(ImageFilter.GaussianBlur(25)).show()
    
