import io
import sqlite3
import panel as pn
import matplotlib.pyplot as plt
import os
from refractivesqlite import dboperations as DB
from Calculo import calculate_mie_arrays  # Import the function from Calculo.py

# Ruta a la base de datos
db_path = r'C:\Users\sersa\Desktop\UC\tfg\tfg\mieWeb\refractive.db'


# Función para conectar a la base de datos y obtener los nombres de los materiales y sus páginas
def obtener_nombres_materiales():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Consultar los nombres de los materiales y sus páginas
    cursor.execute("SELECT pageid, book FROM pages")

    # Obtener todos los resultados
    materiales = cursor.fetchall()

    conn.close()

    # Usar un conjunto para rastrear nombres únicos y un diccionario para los resultados
    nombres_vistos = set()
    material_dict = {}

    for material in materiales:
        pageid, nombre = material
        if nombre not in nombres_vistos:
            material_dict[nombre] = pageid
            nombres_vistos.add(nombre)

    # Ordenar la lista de nombres únicos alfabéticamente
    nombres_unicos = sorted(material_dict.keys())

    return nombres_unicos, material_dict


# Obtener los nombres de los materiales y el diccionario de materiales
nombres_materiales, material_dict = obtener_nombres_materiales()

# Crear un widget de selección múltiple con Panel
multi_choice = pn.widgets.MultiChoice(name="Seleccionar Materiales", options=nombres_materiales, width=400,
                                      placeholder="Seleccione los materiales que desee")

# Contenedor para los widgets de selección de páginas
page_selectors = pn.Column()

# Diccionario para almacenar los valores de lambda, n y k para cada página
material_data = {}

# Variable to store the radius value
radius_value = None

# Create a Matplotlib pane to display the plot
fig, ax = plt.subplots()
ax.set_xlabel('Wavelength')
ax.set_ylabel('qext')
plot_pane = pn.pane.Matplotlib(fig, width=650, height=650)


# Función para actualizar el gráfico
def actualizar_plot():
    if radius_value is None:
        return  # No hacer nada si el valor del radio no está definido

    # Limpiar el gráfico antes de dibujar nuevas curvas
    ax.clear()
    ax.set_xlabel('Wavelength')
    ax.set_ylabel('qext')

    # Dibujar las curvas para todos los materiales en el diccionario
    for material_name, data in material_data.items():
        results = calculate_mie_arrays(data, float(radius_value))
        ax.plot(data['lambda'], results['qext'], label=f'qext {material_name} ')

    # Añadir leyenda y actualizar el gráfico
    ax.legend()
    plot_pane.object = fig


# Función para manejar la entrada del radio
def store_radius(event):
    global radius_value
    try:
        # Intentar convertir el valor introducido a float
        radius_value = float(radius_input.value)

        # Verificar si el radio es mayor que 0
        if radius_value <= 0:
            raise ValueError("El valor del radio debe ser mayor que 0.")

        # Si es válido, actualizar el gráfico
        actualizar_plot()

        # Reseteamos el mensaje de error si el valor es válido
        error_message.object = ""  # Limpiar mensaje de error

    except ValueError as e:
        # Mostrar un mensaje de advertencia si el valor es inválido
        error_message.object = f"Error. Por favor, ingrese un valor válido para el radio."


# Crear una entrada de texto para el radio
radius_input = pn.widgets.TextInput(name='Radio', placeholder='Introduzca el valor del radio en micrómetros')

# Crear un botón para confirmar el radio
confirm_button = pn.widgets.Button(name='Confirmar radio', button_type='primary')

# Crear un mensaje de error (inicialmente vacío)
error_message = pn.pane.Markdown("", width=400, height=50)

# Adjuntar la función store_radius al evento de clic del botón
confirm_button.on_click(store_radius)


# Función que se ejecuta cuando el usuario selecciona materiales
def mostrar_seleccion(event):
    # Obtener los materiales seleccionados
    seleccionados = set(event.new)

    # Eliminar los selectores de páginas de los materiales que ya no están seleccionados
    for widget in list(page_selectors):
        if widget.name.split(" para ")[1] not in seleccionados:
            page_selectors.remove(widget)
            material_data.pop(widget.name.split(" para ")[1], None)

    # Añadir selectores de páginas para los nuevos materiales seleccionados
    for nombre in seleccionados:
        if not any(widget.name.split(" para ")[1] == nombre for widget in page_selectors):
            # Consultar las páginas del material seleccionado
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT pageid, page FROM pages WHERE book = ?", (nombre,))
            paginas = cursor.fetchall()
            conn.close()

            # Crear un selector para las páginas del material
            opciones_paginas = ['Seleccione página'] + [pagina[1] for pagina in paginas]
            page_selector = pn.widgets.Select(name=f"Seleccionar página para {nombre}", options=opciones_paginas,
                                              value='Seleccione página')
            page_selectors.append(page_selector)

            # Función para actualizar los valores de lambda, n y k cuando se selecciona una página
            def actualizar_valores(event, nombre=nombre):
                if event.new != 'Seleccione página':
                    page_name = event.new
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    cursor.execute("SELECT pageid FROM pages WHERE page = ? AND book = ?", (page_name, nombre))
                    page_id = cursor.fetchone()[0]
                    conn.close()
                    db = DB.Database(db_path)
                    lambda_array = db.get_material_n_numpy(page_id)[:, 0]  # Suponiendo que la primera columna es lambda
                    n_array = db.get_material_n_numpy(page_id)[:, 1]
                    k_array = db.get_material_k_numpy(page_id)[:, 1]
                    material_data[nombre] = {
                        'lambda': lambda_array,
                        'n': n_array,
                        'k': k_array,
                        'page_id': page_id
                    }
                    # Actualizar el gráfico después de agregar los nuevos datos
                    actualizar_plot()

            # Conectar el evento al selector de páginas
            page_selector.param.watch(actualizar_valores, 'value')

    # Actualizar el gráfico con todos los materiales seleccionados
    actualizar_plot()


# Conectar la función de selección a los multi-choice
multi_choice.param.watch(mostrar_seleccion, 'value')

# Función para generar la imagen de la gráfica
def generar_imagen():
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return buf

# Crear el botón de descarga
download_button = pn.widgets.FileDownload(filename='grafica.png', callback=generar_imagen, button_type='primary', name='Descargar gráfica')

# Crear el layout de Panel (añadir el botón de descarga)
layout = pn.Row(
    pn.Column(multi_choice, page_selectors),
    pn.Column(radius_input, confirm_button, error_message, plot_pane, download_button)  # Añadir download_button aquí
)

# Mostrar el layout
pn.extension()
layout.show()



