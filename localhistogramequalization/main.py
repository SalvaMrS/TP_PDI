import cv2
import numpy as np


class LocalHistogramEqualizer:
    def __init__(self, image_path, window_size):
        self.image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        self.window_size = window_size

    def equalize(self):
        pass

    def show_input_image(self):
        pass

    def show_output_image(self, output_image):
        pass
