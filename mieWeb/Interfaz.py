import sqlite3
import panel as pn
from refractivesqlite import dboperations as DB

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

# Función que se ejecuta cuando el usuario selecciona materiales
def mostrar_seleccion(event):
    # Obtener los materiales seleccionados
    seleccionados = set(event.new)

    # Eliminar los selectores de páginas de los materiales que ya no están seleccionados
    for widget in list(page_selectors):
        if widget.name.split(" para ")[1] not in seleccionados:
            page_selectors.remove(widget)

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
            page_selector = pn.widgets.Select(name=f"Seleccionar página para {nombre}", options=opciones_paginas, value='Seleccione página')
            page_selectors.append(page_selector)

            # Función para actualizar los valores de lambda, n y k cuando se selecciona una página
            def actualizar_valores(event):
                if event.new != 'Seleccione página':
                    page_name = event.new
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    cursor.execute("SELECT pageid FROM pages WHERE page = ? AND book = ?", (page_name, nombre))
                    page_id = cursor.fetchone()[0]
                    conn.close()
                    db = DB.Database(db_path)
                    lambda_array = db.get_material_n_numpy(page_id)[:, 0]  # Assuming the first column is lambda
                    n_array = db.get_material_n_numpy(page_id)[:, 1]
                    k_array = db.get_material_k_numpy(page_id)[:, 1]
                    material_data[page_id] = {
                        'lambda': lambda_array,
                        'n': n_array,
                        'k': k_array
                    }
                    # Print the values to verify
                    print(f"Page ID: {page_id}")
                    print(f"Lambda: {lambda_array}")
                    print(f"n: {n_array}")
                    print(f"k: {k_array}")

            # Conectar la función de actualización al selector de páginas
            page_selector.param.watch(actualizar_valores, 'value')

# Conectar la función de selección a los multi-choice
multi_choice.param.watch(mostrar_seleccion, 'value')

# Mostrar los widgets
pn.extension()
pn.Column(multi_choice, page_selectors).show()