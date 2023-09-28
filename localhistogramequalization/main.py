import cv2
import numpy as np
import logging


def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Crear un archivo de registro
    handler = logging.FileHandler('local_histogram_equalizer.log')
    handler.setLevel(logging.DEBUG)

    # Formato de registro
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Agregar el manejador al registro
    logger.addHandler(handler)
    return logger


class LocalHistogramEqualizer:
    def __init__(self, image_path, window_size):
        self.image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        self.window_size = window_size
        self.logger = setup_logger()

    def equalize(self):
        try:
            height, width = self.image.shape[:2]
            half_window = self.window_size // 2
            output_image = np.copy(self.image)

            for y in range(half_window, height - half_window):
                for x in range(half_window, width - half_window):
                    roi = self.image[y - half_window:y + half_window + 1, x - half_window:x + half_window + 1]
                    hist, _ = np.histogram(roi.flatten(), bins=256, range=(0, 256))
                    if hist.max() == 0:
                        continue
                    cdf = hist.cumsum()
                    if (cdf.max() - cdf.min()) == 0:
                        continue
                    cdf_normalized = (cdf - cdf.min()) * 255 / (cdf.max() - cdf.min())
                    output_image[y, x] = cdf_normalized[roi[0, 0]]

            return output_image
        except Exception as e:
            self.logger.error(f'Error en la ecualización local del histograma: {str(e)}')
            return None

    def show_input_image(self):
        try:
            cv2.imshow('Imagen de Entrada', self.image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        except Exception as e:
            self.logger.error(f'Error al mostrar la imagen de entrada: {str(e)}')

    def show_output_image(self, output_image):
        try:
            cv2.imshow('Imagen Procesada', output_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        except Exception as e:
            self.logger.error(f'Error al mostrar la imagen procesada: {str(e)}')


# Ejemplo de uso:
image_path = 'imagen.png'
window_size = 15
equalizer = LocalHistogramEqualizer(image_path, window_size)
output_image = equalizer.equalize()
if output_image is not None:
    equalizer.show_input_image()
    equalizer.show_output_image(output_image)
