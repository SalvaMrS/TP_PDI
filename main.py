import logging
from formfieldextractor.fieldextractor import FormFieldExtractor
from localhistogramequalization.histogramequalization import LocalHistogramEqualizer

# Configuración del logger
def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Crear un archivo de registro
    handler = logging.FileHandler('main.log')
    handler.setLevel(logging.DEBUG)

    # Formato de registro
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Agregar el manejador al registro
    logger.addHandler(handler)
    return logger

logger = setup_logger()

# Imágenes disponibles
imagenes = {
    1: 'Imagenes/formulario_01.png',
    2: 'Imagenes/formulario_02.png',
    3: 'Imagenes/formulario_03.png',
    4: 'Imagenes/formulario_04.png',
    5: 'Imagenes/formulario_05.png',
    6: 'Imagenes/formulario_vacio.png'
}

# Opción 1: Ecualización local de histograma
def opcion_1():
    try:
        window_size = int(input("Selecciona un tamaño de ventana para el Ejercicio 1: "))
        image_path = 'Imagenes/Imagen_con_detalles_escondidos.tif'
        equalizer = LocalHistogramEqualizer(image_path, window_size)
        equalizer.show_images()

    except ValueError as ve:
        print(f"Error: {ve}")
        logger.error(f"Error en el Ejercicio 1: {ve}")
    except Exception as e:
        logger.error(f"Error en el Ejercicio 1: {str(e)}")

# Opción 2: Validación de formulario
def opcion_2():
    while True:
        print('Seleccione una imagen para analizar: ')
        for key, value in imagenes.items():
            print(f'{key}. {value}')

        seleccion = input("Elija la imagen a analizar ('p' para regresar al menú anterior o 's' para salir): ")

        if seleccion.lower() == 'p':
            break  

        if seleccion.lower() == 's':
            print("Saliendo de la opción 2...")
            return  # Salir de la función opcion_2

        try:
            seleccion = int(seleccion)
            imagen = imagenes.get(seleccion, '')

            if imagen:
                extractor = FormFieldExtractor(imagen)
                resultados = extractor.extract_form_fields()
                            
                for idx, (campo, resultado) in enumerate(resultados, 1):
                    print(f"{idx}. {campo}:\t{resultado}")
            
        except ValueError as ve:
            print(f"Error: {ve}")
            logger.error(f"Error en la Opción 2: {ve}")

# Menú principal
def menu():
    while True:
        print("\nMenú:")
        print("1) Ecualización local de histograma")
        print("2) Validación de formulario")
        print("s) Salir")

        opcion = input("Selecciona una opción (1, 2, o s para salir): ")

        if opcion == '1':
            opcion_1()
        elif opcion == '2':
            opcion_2()
        elif opcion.lower() == 's':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Selecciona 1, 2, o s para salir.")

if __name__ == "__main__":
    menu()
