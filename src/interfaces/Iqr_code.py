from abc import ABC, abstractmethod


class IQRCode(ABC):
    @abstractmethod
    def generate(self) -> None:
        pass
