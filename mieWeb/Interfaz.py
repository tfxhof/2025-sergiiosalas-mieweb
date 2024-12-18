import io
import sqlite3
import panel as pn
from bokeh.plotting import figure
from bokeh.models import HoverTool, LegendItem
from bokeh.io import output_notebook


from refractivesqlite import dboperations as DB
from Calculo import calculate_mie_arrays  # Import the function from Calculo.py
from bokeh.palettes import Category10
from bokeh.models import Legend

# Ruta a la base de datos
db_path = r'C:\Users\sersa\Desktop\UC\tfg\tfg\mieWeb\refractive.db'

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

# Variable para almacenar el n del medio
n_surrounding_value = 1.0  # Valor predeterminado

# Initialize Bokeh output
output_notebook()


# Create a Bokeh figure with fixed dimensions
plot = figure(
    x_axis_label='Wavelength (nm)',
    y_axis_label='qext',
    tools="pan,box_zoom,reset,hover",
    tooltips=[("Wavelength", "@x"), ("Value", "@y")],
    width=500,  # Fixed width
    height=500  # Fixed height
)


def actualizar_plot():
    plot.renderers = []  # Clear previous renderers
    plot.yaxis.axis_label = plot_option.value  # Update y-axis label

    if radius_value is None:
        return

    colors = Category10[10]  # Use a color palette with 10 colors
    color_index = 0
    legend_items = []

    for material_name, data in material_data.items():
        results = calculate_mie_arrays(data, float(radius_value), float(n_surrounding_value))
        x = data['lambda']
        y = results[plot_option.value]
        color = colors[color_index % len(colors)]  # Cycle through colors
        line = plot.line(x, y, line_width=2, color=color)
        legend_items.append(LegendItem(label=f'{plot_option.value} {material_name}', renderers=[line]))
        color_index += 1

    # Crear la leyenda y añadirla a la gráfica
    legend = Legend(items=legend_items, location="top_right")  # Ajusta la ubicación de la leyenda
    plot.add_layout(legend, 'center')  # 'center' coloca la leyenda sobre la gráfica

# Crear el contenedor para la gráfica sin leyenda
plot_pane = pn.pane.Bokeh(plot, sizing_mode="stretch_both", min_height=400, min_width=400, max_height=50, max_width=500)

# Añadimos un RadioButtonGroup para seleccionar qué graficar
plot_option = pn.widgets.RadioBoxGroup(
    name='Seleccionar métrica a graficar',
    options=['qext', 'qsca', 'qabs'],
    value='qext',  # Valor predeterminado
    inline=True
)

# Conectar el RadioButtonGroup para actualizar la gráfica cuando se cambie la opción
plot_option.param.watch(lambda event: actualizar_plot(), 'value')

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
    name='Radio (nm)',
    placeholder='Introduzca el valor del radio en nanómetros',
    ##sizing_mode="stretch_width"
    width=300,
)

# Botón para confirmar el radio
confirm_radius_button = pn.widgets.Button(
    name='Confirmar radio',
    button_type='primary',
    ##sizing_mode="stretch_width",
    width=50
)

# Adjuntar la función store_radius al evento del botón
confirm_radius_button.on_click(store_radius)

# Función para manejar la entrada del n del medio
def store_n_surrounding(event):
    global n_surrounding_value
    try:
        n_surrounding_value = float(n_surrounding_input.value) if n_surrounding_input.value else 1.0
        if n_surrounding_value <= 0:
            raise ValueError("El valor de n del medio debe ser mayor que 0.")
        actualizar_plot()
        error_message.object = ""
    except ValueError:
        error_message.object = "Error: Ingrese un valor válido para el n del medio."

# Crear una entrada de texto para el n del medio
n_surrounding_input = pn.widgets.TextInput(
    name='n del medio',
    placeholder='Introduzca el valor de n del medio',
    value='1',  # Valor predeterminado
    ##sizing_mode="stretch_width"
    width=300,
)

# Botón para confirmar el n del medio
confirm_n_surrounding_button = pn.widgets.Button(
    name='Confirmar n del medio',
    button_type='primary',
    ##sizing_mode="stretch_width",
    width=50
)

# Adjuntar la función store_n_surrounding al evento del botón
confirm_n_surrounding_button.on_click(store_n_surrounding)

# Mensaje de error
error_message = pn.pane.Markdown("", sizing_mode="stretch_width")

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
                width=200
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
    plot.output_backend = "png"
    plot.save(buffer)
    buffer.seek(0)
    return buffer

# Botón de descarga para la gráfica
download_button = pn.widgets.FileDownload(
    filename='grafica.png',
    callback=descargar_grafica,
    button_type='primary',
    ##sizing_mode="stretch_width"
)

# Actualizar el layout para incluir el RadioButtonGroup encima de la gráfica
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
                confirm_radius_button,  # Botón para confirmar el radio
                sizing_mode='fixed',  # Tamaño fijo para que el botón no estire
                margin=(16, 0, 0, 0)  # Eliminar márgenes adicionales
            ),
        ),
        pn.Row(
            n_surrounding_input,  # Entrada para el n del medio
            pn.Column(  # Usamos un Column para aplicar un espaciado
                confirm_n_surrounding_button,  # Botón para confirmar el n del medio
                sizing_mode='fixed',  # Tamaño fijo para que el botón no estire
                margin=(16, 0, 0, 0)  # Eliminar márgenes adicionales
            ),
        ),
        pn.Row(
            error_message,  # Mensaje de error
        ),
        pn.Column(
              # Añadir el RadioButtonGroup para seleccionar la métrica
            pn.Row(
                plot_option,
                # Usamos un Column para aplicar un espaciado
                download_button,  # Botón de descarga
                align='center',
            ),
            pn.Row(
                plot_pane,  # Gráfica
            ),
        ),
        max_width=1000 # Ancho fijo para esta columna
    ),
    sizing_mode="stretch_width"  # Se adapta al tamaño de la pantalla
)

# Mostrar el layout
pn.extension()
layout.show()