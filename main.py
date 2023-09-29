from formfieldextractor.main import FormFieldExtractor
from localhistogramequalization.main import LocalHistogramEqualizer

window_size = 20
image_path = 'Imagenes/Imagen_con_detalles_escondidos.tif'
equalizer = LocalHistogramEqualizer(image_path, window_size)
equalizer.show_images()

"""output_image = equalizer.equalize()
equalizer.show_input_image()
equalizer.show_output_image(output_image)
equalizer.close()"""

image_path_1 = 'Imagenes/formulario_05.png'
extractor = FormFieldExtractor(image_path_1)
resultados = extractor.extract_form_fields()

for idx, (campo, resultado) in enumerate(resultados, 1):
    print(f"{idx}. {campo}:\t{resultado}")
