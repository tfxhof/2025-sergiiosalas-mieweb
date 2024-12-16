import io
import sqlite3
import panel as pn
import matplotlib.pyplot as plt
import pylab as p

from refractivesqlite import dboperations as DB
from Calculo import calculate_mie_arrays  # Import the function from Calculo.py

# Ruta a la base de datos
db_path = r'C:\Users\sersa\Desktop\UC\tfg\tfg\mieWeb\refractive2.db'

# Función para conectar a la base de datos y obtener los nombres de los materiales y sus páginas
def obtener_nombres_materiales():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT pageid, book FROM pages")
    materiales = cursor.fetchall()
    conn.close()
    nombres_vistos = set()
    material_dict = {}
    for material in materiales:
        pageid, nombre = material
        if nombre not in nombres_vistos:
            material_dict[nombre] = pageid
            nombres_vistos.add(nombre)
    nombres_unicos = sorted(material_dict.keys())
    return nombres_unicos, material_dict

# Obtener los nombres de los materiales y el diccionario de materiales
nombres_materiales, material_dict = obtener_nombres_materiales()

# Crear un widget de selección múltiple con Panel
multi_choice = pn.widgets.MultiChoice(
    name="Seleccionar Materiales",
    options=nombres_materiales,
    width=350,
    placeholder="Seleccione los materiales que desee",
    ##sizing_mode="stretch_width"
)

# Contenedor para los widgets de selección de páginas
page_selectors = pn.Column(sizing_mode="stretch_width")

# Diccionario para almacenar los valores de lambda, n y k para cada página
material_data = {}

# Variable para almacenar el radio
radius_value = None

# Crear un gráfico de Matplotlib adaptable
fig, ax = plt.subplots()
ax.set_xlabel('Wavelength')
ax.set_ylabel('qext')
plot_pane = pn.pane.Matplotlib(
    fig,
    sizing_mode="stretch_width",
    min_height=600,
    min_width= 500,
    max_width = 700,
)

# Función para actualizar el gráfico
def actualizar_plot():
    if radius_value is None:
        return
    ax.clear()
    ax.set_xlabel('Wavelength')
    ax.set_ylabel('qext')
    for material_name, data in material_data.items():
        results = calculate_mie_arrays(data, float(radius_value))
        ax.plot(data['lambda'], results['qext'], label=f'qext {material_name}')
    ax.legend()
    plot_pane.object = fig

# Función para manejar la entrada del radio
def store_radius(event):
    global radius_value
    try:
        radius_value = float(radius_input.value)
        if radius_value <= 0:
            raise ValueError("El valor del radio debe ser mayor que 0.")
        actualizar_plot()
        error_message.object = ""
    except ValueError:
        error_message.object = "Error: Ingrese un valor válido para el radio."

# Crear una entrada de texto para el radio
radius_input = pn.widgets.TextInput(
    name='Radio',
    placeholder='Introduzca el valor del radio en micrómetros',
    ##sizing_mode="stretch_width"
    width = 300,
)

# Botón para confirmar el radio
confirm_button = pn.widgets.Button(
    name='Confirmar radio',
    button_type='primary',
    ##sizing_mode="stretch_width",
    width = 50
)

# Mensaje de error
error_message = pn.pane.Markdown("", sizing_mode="stretch_width")

# Adjuntar la función store_radius al evento del botón
confirm_button.on_click(store_radius)

# Función que se ejecuta cuando el usuario selecciona materiales
def mostrar_seleccion(event):
    seleccionados = set(event.new)
    for widget in list(page_selectors):
        if widget.name.split(" para ")[1] not in seleccionados:
            page_selectors.remove(widget)
            material_data.pop(widget.name.split(" para ")[1], None)
    for nombre in seleccionados:
        if not any(widget.name.split(" para ")[1] == nombre for widget in page_selectors):
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT pageid, page FROM pages WHERE book = ?", (nombre,))
            paginas = cursor.fetchall()
            conn.close()
            opciones_paginas = ['Seleccione página'] + [pagina[1] for pagina in paginas]
            page_selector = pn.widgets.Select(
                name=f"Seleccionar página para {nombre}",
                options=opciones_paginas,
                value='Seleccione página',
                ##sizing_mode="stretch_width",
                width = 200
            )
            page_selectors.append(page_selector)

            def actualizar_valores(event, nombre=nombre):
                if event.new == 'Seleccione página':
                    material_data.pop(nombre, None)
                else:
                    page_name = event.new
                    try:
                        conn = sqlite3.connect(db_path)
                        cursor = conn.cursor()
                        cursor.execute("SELECT pageid FROM pages WHERE page = ? AND book = ?", (page_name, nombre))
                        page_id = cursor.fetchone()[0]
                        conn.close()
                        db = DB.Database(db_path)
                        lambda_array = db.get_material_n_numpy(page_id)[:, 0]
                        n_array = db.get_material_n_numpy(page_id)[:, 1]
                        k_array = db.get_material_k_numpy(page_id)[:, 1]
                        material_data[nombre] = {
                            'lambda': lambda_array,
                            'n': n_array,
                            'k': k_array,
                            'page_id': page_id
                        }
                    except Exception as e:
                        error_message.object = f"Error al seleccionar la página: {str(e)}"
                actualizar_plot()

            page_selector.param.watch(actualizar_valores, 'value')
    actualizar_plot()

# Conectar la función mostrar_seleccion al multi-choice
multi_choice.param.watch(mostrar_seleccion, 'value')

# Función de callback para la descarga de la gráfica
def descargar_grafica():
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    return buffer

# Botón de descarga para la gráfica
download_button = pn.widgets.FileDownload(
    filename='grafica.png',
    callback=descargar_grafica,
    button_type='primary',
    ##sizing_mode="stretch_width"
)

# Crear el layout ajustado sin `spacing`
layout = pn.Row(
    # Columna izquierda: Selector de materiales y páginas
    pn.Column(
        multi_choice,  # Selector de materiales
        page_selectors,  # Selectores de páginas dinámicos
        width=400  # Ancho fijo para esta columna
    ),
    # Columna central: Radio, gráfica y botón de descarga
    pn.Column(
        pn.Row(
            radius_input,  # Entrada para el radio
            pn.Column(  # Usamos un Column para aplicar un espaciado
                confirm_button,  # Botón para confirmar el radio
                sizing_mode='fixed',  # Tamaño fijo para que el botón no estire
                margin=(16, 0, 0, 0)  # Eliminar márgenes adicionales
            ),
        ),
        pn.Row (
            error_message,  # Mensaje de error
        ),

        pn.Column (
            pn.Row(  # Usamos un Column para aplicar un espaciado
                download_button,  # Botón de descarga
                align = 'center',
            ),

            pn.Row(
                plot_pane,  # Gráfica
            ),
        ),


        max_width=700  # Ancho fijo para esta columna
    ),
    sizing_mode="stretch_width"  # Se adapta al tamaño de la pantalla
)

# Mostrar el layout
pn.extension()
layout.show()