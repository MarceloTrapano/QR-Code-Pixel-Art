from abc import ABC, abstractmethod
from PIL import Image


class IImageJoinFactory(ABC):
    @abstractmethod
    def build(self, url: str, image: Image) -> None:
        pass
