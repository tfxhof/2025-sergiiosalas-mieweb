import sqlite3

import panel as pn
from bokeh.models import LegendItem
from bokeh.palettes import Category10
from bokeh.models import Legend

from AccesoDatos import obtener_nombres_materiales
from Calculo import calculate_mie_arrays
from refractivesqlite import dboperations as DB

# Obtener los nombres de los materiales y el diccionario de materiales
nombres_materiales, material_dict = obtener_nombres_materiales()

# Diccionario para almacenar los valores de lambda, n y k para cada página
material_data = {}

# Variable para almacenar el radio
radius_value = None

# Variable para almacenar el n del medio
n_surrounding_value = 1.0  # Valor predeterminado

# Mensaje de error
error_message = pn.pane.Markdown("", sizing_mode="stretch_width")


def actualizar_plot(plot, plot_option, radius_value):
    plot.renderers = []  # Clear previous renderers
    plot.yaxis.axis_label = plot_option.value  # Update y-axis label

    if radius_value is None:
        return

    colors = Category10[10]  # Use a color palette with 10 colors
    color_index = 0
    legend_items = []

    # Eliminar las leyendas existentes
    plot.legend.items = []

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

db_path = r'C:\Users\sersa\Desktop\UC\tfg\tfg\mieWeb\refractive.db'
# Función que se ejecuta cuando el usuario selecciona materiales
def mostrar_seleccion(event, page_selectors,plot, plot_option):
    seleccionados = set(event.new)
    for widget in list(page_selectors):
        nombre_material = widget.name.split(" for ")[1]
        if nombre_material not in seleccionados:  # Si el material fue deseleccionado
            page_selectors.remove(widget)  # Eliminar el selector de página
            material_data.pop(nombre_material, None)  # Eliminar el material de `material_data`

    for nombre in seleccionados:
        if not any(widget.name.split(" for ")[1] == nombre for widget in page_selectors):
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT pageid, page FROM pages WHERE book = ?", (nombre,))
            paginas = cursor.fetchall()
            conn.close()
            opciones_paginas = ['Select page'] + [pagina[1] for pagina in paginas]
            page_selector = pn.widgets.Select(
                name=f"Select page for {nombre}",
                options=opciones_paginas,
                value='Select page',
                width=200
            )
            page_selectors.append(page_selector)

            def actualizar_valores(event, nombre=nombre):
                if event.new == 'Select page':
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
                            'lambda': lambda_array * 1000,  # Convertir a nm
                            'n': n_array,
                            'k': k_array,
                            'page_id': page_id,
                            'page_name': page_name
                        }
                    except Exception as e:
                        error_message.object = f"Error: {str(e)}"
                actualizar_plot(plot, plot_option, radius_value)

            page_selector.param.watch(actualizar_valores, 'value')
    actualizar_plot(plot, plot_option, radius_value)
