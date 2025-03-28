import tempfile
import zipfile
from bokeh.io import export_svg


from src.negocio.calculo import calculate_mie_arrays



def descargar_txt(presenter_instance):
    try:
        # Crear un archivo ZIP temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp_zip:
            with zipfile.ZipFile(tmp_zip, 'w') as zipf:
                # Iterar sobre los materiales en la gráfica
                for material_name, data in presenter_instance.material_data.items():
                    # Obtener los valores de lambda y los resultados de qext, qabs, y qsca
                    lambda_values = data['lambda']  # Convertir a nm
                    results = calculate_mie_arrays(data, float(presenter_instance.radius_value), float(presenter_instance.n_surrounding_value))
                    qext_values = results['qext']
                    qabs_values = results['qabs']
                    qsca_values = results['qsca']

                    page_name = presenter_instance.material_data[material_name].get('page_name', 'Unknown page')

                    # Crear el contenido del archivo TXT con columnas alineadas
                    # Formateo con un ancho fijo de 30 caracteres por columna para acomodar números largos
                    txt_content1 = "{:<30}{:<30}{:<30}{:<30}\n".format("lambda_nm", "qext", "qabs", "qsca")
                    for i in range(len(lambda_values)):
                        txt_content1 += "{:<30.8f}{:<30.8f}{:<30.8f}{:<30.8f}\n".format(
                            lambda_values[i], qext_values[i], qabs_values[i], qsca_values[i]
                        )

                    # Crear el nombre del archivo TXT
                    txt_filename = f"{material_name}_{page_name}.txt"

                    # Añadir el archivo TXT al ZIP
                    zipf.writestr(txt_filename, txt_content1)

            # Establecer el nombre del archivo ZIP
            zip_filename = tmp_zip.name

        return zip_filename
    except Exception as e:
        print( f"Error: {str(e)}")





