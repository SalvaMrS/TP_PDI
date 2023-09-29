import cv2
import numpy as np
import matplotlib.pyplot as plt

# Ruta de la imagen del formulario
ruta_imagen = 'Imagenes/formulario_02.png'

# Cargar la imagen en escala de grises
imagen = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)

# Calcular el promedio de cada fila
promedios_filas = np.mean(imagen, axis=1)

# Dibujar una línea en cada fila donde el promedio es menor a 100
umbral_promedio = 100
coordenadas_lineas = []  # Almacenar las coordenadas de las líneas
recortes = []  # Lista para almacenar los recortes

for i, promedio in enumerate(promedios_filas):
    if promedio < umbral_promedio:
        # Almacenar las coordenadas de las líneas
        coordenadas_lineas.append(i)
        
        if len(coordenadas_lineas) > 1:
            # Recortar la imagen en áreas definidas por las líneas, ajustando las coordenadas
            inicio = coordenadas_lineas[-2] + 2  # Añadir 2 para evitar las 2 líneas anteriores
            fin = coordenadas_lineas[-1] - 2     # Restar 2 para evitar las 2 líneas siguientes
            seccion = imagen[inicio:fin, :]
            recortes.append(seccion)

# Descartar los recortes 1 y 6
del recortes[0]  # Descartar el primer recorte (índice 0)
del recortes[4]  # Descartar el sexto recorte (índice 4)

# Conservar solo la parte entre la segunda línea divisoria y la última
recortes_conservados = []

for recorte in recortes:
    # Encontrar la segunda línea divisoria
    coordenadas_lineas_columnas = []  # Almacenar las coordenadas de las líneas en el recorte
    promedios_columnas_recorte = np.mean(recorte, axis=0)
    
    for j, promedio in enumerate(promedios_columnas_recorte):
        if promedio < umbral_promedio:
            coordenadas_lineas_columnas.append(j)
    
    # Conservar la parte entre la segunda línea divisoria y la última
    if len(coordenadas_lineas_columnas) >= 2:
        inicio = coordenadas_lineas_columnas[1] + 2  # Añadir 1 para evitar la línea anterior
        fin = coordenadas_lineas_columnas[-1] - 2    # Restar 1 para evitar la línea siguiente
        recorte_conservado = recorte[:, inicio:fin]
        recortes_conservados.append(recorte_conservado)

def count_caracter(recorte):
    # Binarizar el recorte (cambiar umbral si es necesario)
    _, binarizado = cv2.threshold(recorte, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Etiquetar componentes conectados en el recorte
    num_etiquetas, _, _, _ = cv2.connectedComponentsWithStats(binarizado, connectivity=4, ltype=cv2.CV_32S)

    # Restar 1 para excluir la etiqueta 0 (fondo)
    num_caracteres = num_etiquetas - 1

    return num_caracteres

def count_word(recorte):
    # Binarizar el recorte (cambiar umbral si es necesario)
    _, binarizado = cv2.threshold(recorte, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Encontrar los contornos de los caracteres
    contornos, _ = cv2.findContours(binarizado, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    distancia_umbral = 5  # Umbral de distancia entre caracteres para considerar una palabra
    num_palabras = 0

    if len(contornos) > 0:
        # Ordenar los contornos de izquierda a derecha
        contornos = sorted(contornos, key=lambda x: cv2.boundingRect(x)[0])

        # Calcular la distancia entre el borde derecho de un caracter y el borde izquierdo del siguiente
        for i in range(len(contornos) - 1):
            x1, _, w1, _ = cv2.boundingRect(contornos[i])
            x2, _, _, _ = cv2.boundingRect(contornos[i + 1])
            distancia_entre_caracteres = x2 - (x1 + w1)

            # Si la distancia es mayor que el umbral, considerarlo como una nueva palabra
            if distancia_entre_caracteres > distancia_umbral:
                num_palabras += 1

        # Contar la última palabra (si la hubiera)
        num_palabras += 1

    return num_palabras

# Nombres de los campos correspondientes a cada recorte
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

# Crear una lista para almacenar los resultados
resultados = []

# Verificar las condiciones para cada recorte
for idx, recorte in enumerate(recortes_conservados, 1):
    num_caracteres = count_caracter(recorte)
    num_palabras = count_word(recorte)

    if idx == 1 and 2 >= num_palabras <= 25:
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

# Imprimir los resultados en el formato especificado
for idx, resultado in enumerate(resultados, 1):
    print(f"{idx}. {nombres_campos[idx-1]}:\t{resultado}")
