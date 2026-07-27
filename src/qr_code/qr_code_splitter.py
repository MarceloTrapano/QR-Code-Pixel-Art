from interfaces import IQRCodeSplitter
import cv2
import numpy as np
from PIL import Image


class QRCodeSplitter(IQRCodeSplitter):
    SQUARE_SIZE = 27
    MARKINGS_SIZE = 15

    def __init__(self, image):
        super().__init__(image)
        self.width = self.np_image.shape[0]
        self.data_squares = self.width//3

    def extract_squares(self) -> Image:
        square_mask = np.zeros((self.width, self.width), dtype=np.uint8)
        square_mask[:self.SQUARE_SIZE, :self.SQUARE_SIZE] = 255
        square_mask[-self.SQUARE_SIZE:-1, :self.SQUARE_SIZE] = 255
        square_mask[:self.SQUARE_SIZE, -self.SQUARE_SIZE:-1] = 255
        square_mask[:3, :] = 255
        square_mask[:, :3] = 255
        square_mask[:, -3:] = 255
        square_mask[-3:, :] = 255

        pattern = np.array([
        [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
        [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
        [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
        [0,   0,   0, 255, 255, 255, 255, 255, 255, 255, 255, 255,   0,   0,   0],
        [0,   0,   0, 255, 255, 255, 255, 255, 255, 255, 255, 255,   0,   0,   0],
        [0,   0,   0, 255, 255, 255, 255, 255, 255, 255, 255, 255,   0,   0,   0],
        [0,   0,   0, 255, 255, 255,   0,   0,   0, 255, 255, 255,   0,   0,   0],
        [0,   0,   0, 255, 255, 255,   0,   0,   0, 255, 255, 255,   0,   0,   0],
        [0,   0,   0, 255, 255, 255,   0,   0,   0, 255, 255, 255,   0,   0,   0],
        [0,   0,   0, 255, 255, 255, 255, 255, 255, 255, 255, 255,   0,   0,   0],
        [0,   0,   0, 255, 255, 255, 255, 255, 255, 255, 255, 255,   0,   0,   0],
        [0,   0,   0, 255, 255, 255, 255, 255, 255, 255, 255, 255,   0,   0,   0],
        [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
        [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
        [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0]
                        ], dtype=np.uint8)

        res = cv2.matchTemplate(self.np_image, pattern, cv2.TM_CCOEFF_NORMED)
        threshold = 0.95

        markings = np.where(res > threshold)
        for y, x in zip(*markings):
            square_mask[y:y+self.MARKINGS_SIZE, x:x+self.MARKINGS_SIZE] = 255

        return cv2.merge([self.np_image, self.np_image, self.np_image, square_mask])

    def extract_data_layer(self) -> Image:
        square_mask = np.full(self.np_image.shape[:2], 255, dtype=np.uint8)
        square_mask[:self.SQUARE_SIZE, :self.SQUARE_SIZE] = 0
        square_mask[-self.SQUARE_SIZE:, :self.SQUARE_SIZE] = 0
        square_mask[:self.SQUARE_SIZE, -self.SQUARE_SIZE:] = 0

        data_kernel = np.array([[0, 0, 0],
                               [0, 255, 0],
                               [0, 0, 0]])
        data_mask = np.tile(
            data_kernel, (self.data_squares, self.data_squares)).astype(np.uint8)

        combined_mask = cv2.bitwise_and(square_mask, data_mask)

        return cv2.merge([self.np_image, self.np_image, self.np_image, combined_mask])

    def extract_noise_layer(self) -> Image:
        square_mask = np.full(self.np_image.shape[:2], 255, dtype=np.uint8)
        square_mask[:self.SQUARE_SIZE, :self.SQUARE_SIZE] = 0
        square_mask[-self.SQUARE_SIZE:, :self.SQUARE_SIZE] = 0
        square_mask[:self.SQUARE_SIZE, -self.SQUARE_SIZE:] = 0

        noise = 1/20

        noise_mask = np.random.choice(
            [0, 255], size=self.np_image.shape[:2], p=[1-noise, noise]).astype(np.uint8)

        combined_mask = cv2.bitwise_and(square_mask, noise_mask)

        return cv2.merge([self.np_image, self.np_image, self.np_image, combined_mask])
