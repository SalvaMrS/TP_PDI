import cv2
import numpy as np


class LocalHistogramEqualizer:
    def __init__(self, image_path, window_size):
        self.image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        self.window_size = window_size

    def equalize(self):
        height, width = self.image.shape[:2]
        half_window = self.window_size // 2
        output_image = np.copy(self.image)

        for y in range(half_window, height - half_window):
            for x in range(half_window, width - half_window):
                roi = self.image[y - half_window:y + half_window + 1, x - half_window:x + half_window + 1]
                hist, _ = np.histogram(roi.flatten(), bins=256, range=(0, 256))
                if hist.max() == 0:
                    # Evitar la división por cero y manejar este caso de manera adecuada
                    continue
                print(hist)
                # Calcular la función de distribución acumulativa del histograma
                cdf = hist.cumsum()

                # Verificar si la diferencia es cero antes de la normalización
                if (cdf.max() - cdf.min()) == 0:
                    continue

                cdf_normalized = (cdf - cdf.min()) * 255 / (cdf.max() - cdf.min())
                output_image[y, x] = cdf_normalized[roi[0, 0]]

        return output_image

    def show_input_image(self):
        cv2.imshow('Imagen de Entrada', self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def show_output_image(self, output_image):
        cv2.imshow('Imagen Procesada', output_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
