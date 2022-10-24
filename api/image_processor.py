from PIL import Image, ImageFilter


class ImageProcessor:
    @staticmethod
    def blur(image: Image) -> Image:
        # Blurring the image
        return image.filter(ImageFilter.GaussianBlur(25))
    
