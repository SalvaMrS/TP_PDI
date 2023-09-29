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
    """
    Clase para realizar la ecualización local del histograma en una imagen en escala de grises.

    Args:
      image_path (str): Ruta de la imagen de entrada.
      window_size (int): Tamaño de la ventana para la ecualización local.

    Attributes:
      image (numpy.ndarray): La imagen en escala de grises a procesar.
      window_size (int): El tamaño de la ventana para la ecualización local.
    """
    def __init__(self, image_path, window_size):
        self.image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        self.window_size = window_size
        self.logger = setup_logger()

    def equalize(self):
        """
        Realiza la ecualización local del histograma en la imagen de entrada.
        Returns:
           numpy.ndarray: La imagen procesada con ecualización local del histograma, o None si ocurre un error.
        """
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
        """
        Muestra la imagen de entrada en una ventana.

        Raises:
            Exception: Si ocurre un error al mostrar la imagen.
        """
        try:
            cv2.imshow('Imagen de Entrada', self.image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        except Exception as e:
            error_message = f'Error al mostrar la imagen de entrada: {str(e)}'
            self.logger.error(error_message)

    def show_output_image(self, output_image):
        """
        Muestra la imagen procesada en una ventana.

        Args:
            output_image (numpy.ndarray): La imagen procesada.

        Raises:
            Exception: Si ocurre un error al mostrar la imagen.
        """
        try:
            cv2.imshow('Imagen Procesada', output_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        except Exception as e:
            error_message = f'Error al mostrar la imagen procesada: {str(e)}'
            self.logger.error(error_message)

    def close(self):
        """
        Cierra todas las ventanas abiertas.

        Raises:
            Exception: Si ocurre un error al cerrar las ventanas.
        """
        try:
            cv2.destroyAllWindows()
        except Exception as e:
            error_message = f'Error al cerrar todas las ventanas: {str(e)}'
            self.logger.error(error_message)