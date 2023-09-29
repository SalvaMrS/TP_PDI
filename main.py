import os
from formfieldextractor.main import FormFieldExtractor
from localhistogramequalization.main import LocalHistogramEqualizer

directorio_imagenes = './imagenes/'

def menu_1():
    """
    Menu iteractivo de la actividad 1
    """

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        try:
            window_size = input("Tamaño de la ventana ('C' para salir): ")

            if window_size.lower() == 'c':
                break

            image_path = 'Imagenes/Imagen_con_detalles_escondidos.tif'
            equalizer = LocalHistogramEqualizer(image_path, int(window_size))
            equalizer.show_images()

        except ValueError:
            os.system('cls' if os.name == 'nt' else 'clear')
            input("Entrada no válida. Debe ingresar un número o 'C' para salir.")
        
def menu_2():
    """
    Menu iteractivo de la actividad 2
    """

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        archivos_imagenes = [archivo for archivo in os.listdir(directorio_imagenes) if archivo.endswith('.png')]

        print("Seleccione una imagen para analizar:\n")
        
        for i, imagen in enumerate(archivos_imagenes, 1):
            print(f"{i}. {imagen}")

        try:
            seleccion = input("Elija la imagen a analizar ('C' para salir): ")

            if seleccion.lower() == 'c':
                break

            seleccion = int(seleccion)

            if 1 <= seleccion <= len(archivos_imagenes):
                os.system('cls' if os.name == 'nt' else 'clear')
                ruta_imagen_seleccionada = os.path.join(directorio_imagenes, archivos_imagenes[seleccion - 1])

                extractor = FormFieldExtractor(ruta_imagen_seleccionada)
                resultados = extractor.extract_form_fields()

                for idx, (campo, resultado) in enumerate(resultados, 1):
                    print(f"{idx}. {campo}:\t{resultado}")

                input("\nPresione Enter para continuar...")

            else:
                os.system('cls' if os.name == 'nt' else 'clear')
                input("Selección no válida. Debe elegir un número de imagen válido.")

        except ValueError:
            os.system('cls' if os.name == 'nt' else 'clear')
            input("Entrada no válida. Debe ingresar un número o 'C' para salir.")

def Menu_principal():
    """
    Muestra el menu raiz
    """
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        print("Menú Principal:")
        print("1. Actividad 1")
        print("2. Actividad 2\n")

        opcion = input("Seleccione una opción ('C' para salir): ")

        if opcion == "1":
            os.system('cls' if os.name == 'nt' else 'clear')
            input("Has seleccionado Actividad 1.\n") 
            menu_1()

        elif opcion == "2":
            os.system('cls' if os.name == 'nt' else 'clear')
            input("Has seleccionado Actividad 2\n")
            menu_2()

        elif opcion.lower() == "c":
            print("\nCerrando la aplicación. ¡Hasta luego!\n")
            break
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            input("Opción no válida.")

Menu_principal()