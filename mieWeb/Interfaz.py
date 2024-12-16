import io
import sqlite3
import panel as pn
import matplotlib.pyplot as plt
from refractivesqlite import dboperations as DB
from Calculo import calculate_mie_arrays  # Import the function from Calculo.py

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
multi_choice = pn.widgets.MultiChoice(name="Seleccionar Materiales", options=nombres_materiales, width=400, placeholder="Seleccione los materiales que desee")

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
        return
    ax.clear()
    ax.set_xlabel('Wavelength')
    ax.set_ylabel('qext')
    for material_name, data in material_data.items():
        results = calculate_mie_arrays(data, float(radius_value))
        ax.plot(data['lambda'], results['qext'], label=f'qext {material_name} ')
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
    except ValueError as e:
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
            page_selector = pn.widgets.Select(name=f"Seleccionar página para {nombre}", options=opciones_paginas, value='Seleccione página')
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

# Crear el layout de Panel
layout = pn.Row(
    pn.Column(multi_choice, page_selectors),
    pn.Column(
        radius_input,
        confirm_button,
        error_message,
        plot_pane,
        pn.Column(
            download_button,
            align='center',
            sizing_mode='fixed',
            height=40,
            margin=(0, 0, 10, 0)
        )
    )
)

# Mostrar el layout
pn.extension()
layout.show()