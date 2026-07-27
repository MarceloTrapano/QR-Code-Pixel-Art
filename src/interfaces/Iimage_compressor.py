from abc import ABC, abstractmethod


class IImageCompressor(ABC):
    @abstractmethod
    def compress(self) -> None:
        pass
