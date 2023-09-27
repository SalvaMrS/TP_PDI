import cv2
import numpy as np
import matplotlib.pyplot as plt

# Ruta de la imagen del formulario
ruta_imagen = './imagenes/formulario_01.png'

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
            # Recortar la imagen en áreas definidas por las líneas
            inicio = coordenadas_lineas[-2] + 1  # Añadir 1 para evitar la línea anterior
            fin = coordenadas_lineas[-1] - 1     # Restar 1 para evitar la línea siguiente
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
        inicio = coordenadas_lineas_columnas[1] + 1  # Añadir 1 para evitar la línea anterior
        fin = coordenadas_lineas_columnas[-1] - 1    # Restar 1 para evitar la línea siguiente
        recorte_conservado = recorte[:, inicio:fin]
        recortes_conservados.append(recorte_conservado)

# Mostrar los recortes conservados
for idx, recorte in enumerate(recortes_conservados, 1):
    plt.imshow(recorte, cmap='gray')
    plt.title(f"Recorte {idx} - Parte conservada")
    plt.show()
