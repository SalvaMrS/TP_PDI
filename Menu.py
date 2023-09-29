import os

directorio_imagenes = './imagenes/'

while True:
    archivos_imagenes = [archivo for archivo in os.listdir(directorio_imagenes) if archivo.endswith('.png')]

    print("Seleccione una imagen para analizar:")
    
    for i, imagen in enumerate(archivos_imagenes, 1):
        print(f"{i}. {imagen}")

    try:
        seleccion = input("Elija la imagen a analizar ('C' para salir): ")

        if seleccion.lower() == 'c':
            break

        seleccion = int(seleccion)

        if 1 <= seleccion <= len(archivos_imagenes):
            ruta_imagen_seleccionada = os.path.join(directorio_imagenes, archivos_imagenes[seleccion - 1])

            os.system(f'python Actividad_2.py "{ruta_imagen_seleccionada}"')

            input("Presione Enter para continuar...")

        else:
            print("Selección no válida. Debe elegir un número de imagen válido.")

    except ValueError:
        print("Entrada no válida. Debe ingresar un número o 'C' para salir.")
