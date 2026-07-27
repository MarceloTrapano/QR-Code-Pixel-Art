from interfaces import IQRCode
import qrcode


class QRCode(IQRCode):
    def __init__(self, url: str, version: int = 6):
        self.url = url
        self.size = 3
        self.version = version

    def generate(self, filename: str = ""):
        self.qr = qrcode.QRCode(
            version=self.version,
            box_size=self.size,
            border=1,
        )

        self.qr.add_data(self.url)
        self.qr.make(fit=True)

        self.image = self.qr.make_image()
        if self.version != self.qr._version:
            self.version = self.qr._version

        if filename:
            self.image.save(filename)
