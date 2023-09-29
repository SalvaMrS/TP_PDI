import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('imagen', type=str)

args = parser.parse_args()

ruta_imagen = args.imagen

# Carga de imagen
imagen = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)

promedios_filas = np.mean(imagen, axis=1)

# Recortamos la imagen por donde el promedio de valor 
# de las filas sea menor al umbral

umbral_promedio = 100
coordenadas_lineas = []  
recortes = []

for i, promedio in enumerate(promedios_filas):
    if promedio < umbral_promedio:
        coordenadas_lineas.append(i)
        
        if len(coordenadas_lineas) > 1:
            inicio = coordenadas_lineas[-2] + 2
            fin = coordenadas_lineas[-1] - 2
            seccion = imagen[inicio:fin, :]
            recortes.append(seccion)

# Descartamos las secciones que no interesan
del recortes[0]
del recortes[4]

# Realizamos el proceso anterior por cada recorte 
# analizando las lineas verticales

recortes_conservados = []

for recorte in recortes:
    coordenadas_lineas_columnas = []
    promedios_columnas_recorte = np.mean(recorte, axis=0)
    
    for j, promedio in enumerate(promedios_columnas_recorte):
        if promedio < umbral_promedio:
            coordenadas_lineas_columnas.append(j)
    
    if len(coordenadas_lineas_columnas) >= 2:
        inicio = coordenadas_lineas_columnas[1] + 2
        fin = coordenadas_lineas_columnas[-1] - 2
        recorte_conservado = recorte[:, inicio:fin]
        recortes_conservados.append(recorte_conservado)

def count_caracter(recorte):
    _, binarizado = cv2.threshold(recorte, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    num_etiquetas, _, _, _ = cv2.connectedComponentsWithStats(binarizado, connectivity=4, ltype=cv2.CV_32S)

    num_caracteres = num_etiquetas - 1

    return num_caracteres

def count_word(recorte):
    _, binarizado = cv2.threshold(recorte, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    contornos, _ = cv2.findContours(binarizado, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    distancia_umbral = 5  # Umbral de distancia entre caracteres para considerar una palabra
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

# Validamos que los campos 
for idx, recorte in enumerate(recortes_conservados, 1):
    num_caracteres = count_caracter(recorte)
    num_palabras = count_word(recorte)

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


for idx, resultado in enumerate(resultados, 1):
    print(f"{idx}. {nombres_campos[idx-1]}:\t{resultado}")
