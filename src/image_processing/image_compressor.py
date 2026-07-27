from interfaces import IImageCompressor
from PIL import Image


class ImageCompressor(IImageCompressor):
    def __init__(self, image: Image, size: int):
        self.image = image
        self.size = size

    def compress(self):
        self.resized = self.image.resize((self.size, self.size), Image.NEAREST)
        return self.resized
