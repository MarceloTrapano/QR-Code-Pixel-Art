from interfaces import IImageJoinFactory
from image_processing import ImageCompressor
from qr_code import QRCode, QRCodeSplitter

import numpy as np
from PIL import Image


class ImageJoinFactory(IImageJoinFactory):
    PADDING = 3

    def __init__(self, version: int):
        self.version = version

    def build(self, url, image, opacity=0.7):
        self.qr_code = QRCode(url, version=self.version)
        self.qr_code.generate()

        if self.version != self.qr_code.version:
            self.version = self.qr_code.version

        self.splitter = QRCodeSplitter(self.qr_code.image)

        self.splitter.split()

        self.image_compressor = ImageCompressor(
            image, self.splitter.width-self.PADDING*2)
        self.compressed_image = self.image_compressor.compress()

        self._join(opacity)

    def _join(self, opacity):
        image = Image.new(
            "RGBA", (self.splitter.width, self.splitter.width), (0, 0, 0, 0))

        pixelart_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
        pixelart_img = self.image_compressor.resized

        pixelart_layer.paste(pixelart_img, (self.PADDING, self.PADDING))
        image = Image.alpha_composite(image, pixelart_layer)

        squares_img = self._to_pil_rgba(self.splitter.squares)
        image = Image.alpha_composite(image, squares_img)

        data_img = self._to_pil_rgba(self.splitter.data_layer)
        data_img = self._scale_alpha(data_img, opacity)
        image = Image.alpha_composite(image, data_img)

        noise_img = self._to_pil_rgba(self.splitter.noise_layer)
        noise_img = self._scale_alpha(noise_img, opacity)
        image = Image.alpha_composite(image, noise_img)

        self.image = image

    @staticmethod
    def _to_pil_rgba(arr: np.ndarray) -> Image:
        img = Image.fromarray(arr)
        return img.convert("RGBA")

    @staticmethod
    def _scale_alpha(img: Image, opacity: float) -> Image:
        r, g, b, a = img.split()
        a = a.point(lambda px: int(px * opacity))
        return Image.merge("RGBA", (r, g, b, a))
