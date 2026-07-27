from abc import ABC, abstractmethod
from PIL import Image
import numpy as np


class IQRCodeSplitter(ABC):
    def __init__(self, image: Image):
        self.image = image
        self.np_image = np.array(image.convert("L")).astype(np.uint8)

    @abstractmethod
    def extract_noise_layer(self) -> Image:
        pass

    @abstractmethod
    def extract_data_layer(self) -> Image:
        pass

    @abstractmethod
    def extract_squares(self) -> Image:
        pass

    def split(self) -> None:
        self.noise_layer = self.extract_noise_layer()
        self.data_layer = self.extract_data_layer()
        self.squares = self.extract_squares()
