from formfieldextractor.main import FormFieldExtractor
from localhistogramequalization.main import LocalHistogramEqualizer

window_size = 10
image_path = 'Imagenes/Imagen_con_detalles_escondidos.tif'
equalizer = LocalHistogramEqualizer(image_path, window_size)
output_image = equalizer.equalize()
equalizer.show_input_image()
equalizer.show_output_image(output_image)
equalizer.close()

image_path_1 = 'Imagenes/formulario_01.png'
extractor = FormFieldExtractor(image_path_1)
extractor.extract_lines()
extractor.extract_fields()
resultados = extractor.extract_form_fields()

for idx, (campo, resultado) in enumerate(resultados, 1):
    print(f"{idx}. {campo}:\t{resultado}")
