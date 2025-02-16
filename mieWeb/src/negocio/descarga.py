import tempfile
import zipfile
from calculo import calculate_mie_arrays
import panel as pn
from src.negocio.presenter import Presenter, material_data

# Mensaje de error
error_message = pn.pane.Markdown("", sizing_mode="stretch_width")

def descargar_txt(radius_value, n_surrounding_value):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp_zip:
            with zipfile.ZipFile(tmp_zip, 'w') as zipf:
                for material_name, data in material_data.items():
                    lambda_values = data['lambda']
                    results = calculate_mie_arrays(data, float(Presenter.radius_value), float(Presenter.n_surrounding_value))
                    qext_values = results['qext']
                    qabs_values = results['qabs']
                    qsca_values = results['qsca']

                    txt_content = "{:<12} {:<12} {:<12} {:<12}\n".format("lambda (nm)", "qext", "qabs", "qsca")
                    for i in range(len(lambda_values)):
                        txt_content += "{:<12} {:<12} {:<12} {:<12}\n".format(lambda_values[i], qext_values[i],
                                                                              qabs_values[i], qsca_values[i])

                    txt_filename = f"{material_name}.txt"
                    zipf.writestr(txt_filename, txt_content)

            zip_filename = tmp_zip.name

        error_message.object = "Archivos TXT descargados correctamente."
        return zip_filename
    except Exception as e:
        error_message.object = f"Error al descargar los archivos TXT: {str(e)}"
        return None


    # Función para manejar la descarga de la gráfica en formato PDF

def descargar_pdf(event):
        pass

