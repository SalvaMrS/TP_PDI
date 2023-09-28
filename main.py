from localhistogramequalization.main import LocalHistogramEqualizer

window_size = 20
image_path = 'Imagenes/Imagen_con_detalles_escondidos.tif'
equalizer = LocalHistogramEqualizer(image_path, window_size)
output_image = equalizer.equalize()
equalizer.show_input_image()
equalizer.show_output_image(output_image)
equalizer.close()
