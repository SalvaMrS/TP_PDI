import cv2
import numpy as np


class FormFieldExtractor:
    """
    A class for extracting form fields from an image.

    Args:
        image_path (str): The path to the input image.

    Attributes:
        image_path (str): The path to the input image.
        image (numpy.ndarray): The loaded image in grayscale.
        umbral_promedio (int): The threshold for average pixel intensity.
        coordenadas_lineas (list): List of row coordinates for line extraction.
        recortes (list): List of extracted row segments.
        recortes_conservados (list): List of column-conserved row segments.

    Methods:
        extract_lines: Extract rows based on average pixel intensity.
        extract_fields: Extract column-conserved segments from rows.
        count_characters: Count characters in a segment.
        count_words: Count words in a segment.
        extract_form_fields: Extract and validate form fields.
    """

    def __init__(self, image_path):
        self.image_path = image_path
        self.image = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)
        self.umbral_promedio = 100
        self.coordenadas_lineas = []
        self.recortes = []
        self.recortes_conservados = []
        self.extract_lines()
        self.extract_fields()

    def extract_lines(self):
        """
        Extract rows from the input image based on average pixel intensity.
        """
        promedios_filas = np.mean(self.image, axis=1)

        for i, promedio in enumerate(promedios_filas):
            if promedio < self.umbral_promedio:
                self.coordenadas_lineas.append(i)

                if len(self.coordenadas_lineas) > 1:
                    inicio = self.coordenadas_lineas[-2] + 2
                    fin = self.coordenadas_lineas[-1] - 2
                    seccion = self.image[inicio:fin, :]
                    self.recortes.append(seccion)

        del self.recortes[0]
        del self.recortes[4]

    def extract_fields(self):
        """
        Extract column-conserved segments from the rows.
        """
        for recorte in self.recortes:
            coordenadas_lineas_columnas = []
            promedios_columnas_recorte = np.mean(recorte, axis=0)

            for j, promedio in enumerate(promedios_columnas_recorte):
                if promedio < self.umbral_promedio:
                    coordenadas_lineas_columnas.append(j)

            if len(coordenadas_lineas_columnas) >= 2:
                inicio = coordenadas_lineas_columnas[1] + 2
                fin = coordenadas_lineas_columnas[-1] - 2
                recorte_conservado = recorte[:, inicio:fin]
                self.recortes_conservados.append(recorte_conservado)

    @staticmethod
    def count_characters(recorte):
        """
        Count characters in a given segment.

        Args:
            recorte (numpy.ndarray): The segment to count characters in.

        Returns:
            int: The number of characters in the segment.
        """
        _, binarizado = cv2.threshold(recorte, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        num_etiquetas, _, _, _ = cv2.connectedComponentsWithStats(binarizado, connectivity=4, ltype=cv2.CV_32S)
        num_caracteres = num_etiquetas - 1
        return num_caracteres

    @staticmethod
    def count_words(recorte):
        """
        Count words in a given segment.

        Args:
            recorte (numpy.ndarray): The segment to count words in.

        Returns:
            int: The number of words in the segment.
        """
        _, binarizado = cv2.threshold(recorte, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        contornos, _ = cv2.findContours(binarizado, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        distancia_umbral = 5
        num_palabras = 0

        if len(contornos) > 0:
            contornos = sorted(contornos, key=lambda x: cv2.boundingRect(x)[0])

            for i in range(len(contornos) - 1):
                x1, _, w1, _ = cv2.boundingRect(contornos[i])
                x2, _, _, _ = cv2.boundingRect(contornos[i + 1])
                distancia_entre_caracteres = x2 - (x1 + w1)

                if distancia_entre_caracteres > distancia_umbral:
                    num_palabras += 1

            num_palabras += 1

        return num_palabras

    def extract_form_fields(self):
        """
        Extract and validate form fields from the input image.

        Returns:
            list: A list of tuples containing field names and validation results.
        """
        nombres_campos = [
            "Nombre",
            "Edad",
            "Mail",
            "Legajo",
            "Pregunta 1",
            "Pregunta 2",
            "Pregunta 3",
            "Comentarios"
        ]

        resultados = []

        for idx, recorte in enumerate(self.recortes_conservados, 1):
            num_caracteres = self.count_characters(recorte)
            num_palabras = self.count_words(recorte)

            if idx == 1 and num_palabras >= 2 and num_caracteres <= 25:
                resultados.append("OK")
            elif idx == 2 and num_caracteres in (2, 3):
                resultados.append("OK")
            elif idx == 3 and num_palabras == 1 and num_caracteres <= 25:
                resultados.append("OK")
            elif idx == 4 and num_caracteres == 8 and num_palabras == 1:
                resultados.append("OK")
            elif 5 <= idx <= 7 and num_caracteres == 2:
                resultados.append("OK")
            elif idx == 8 and num_caracteres <= 25:
                resultados.append("OK")
            else:
                resultados.append("MAL")

        return [(campo, resultado) for campo, resultado in zip(nombres_campos, resultados)]
