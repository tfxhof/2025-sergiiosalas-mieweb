import os
import sqlite3
from refractivesqlite import dboperations as DB


# Obtener la ruta del directorio actual (donde está acceso_datos.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construir la ruta de la base de datos dentro de la carpeta persistencia
db_path = os.path.join(BASE_DIR, "refractive.db")


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


def obtener_paginas_material(nombre_material):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT page FROM pages WHERE book = ?", (nombre_material,))
    paginas = cursor.fetchall()
    conn.close()
    return paginas

def obtener_datos_pagina(nombre_material, nombre_pagina):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT pageid FROM pages WHERE book = ? AND page = ?", (nombre_material, nombre_pagina))
    resultado = cursor.fetchone()
    conn.close()

    if resultado is None:
        raise ValueError(f"No se encontró la página '{nombre_pagina}' para el material '{nombre_material}'")

    page_id = resultado[0]  # Extraer el ID correctamente


    db = DB.Database(db_path)
    lambda_array = db.get_material_n_numpy(page_id)[:, 0]
    n_array = db.get_material_n_numpy(page_id)[:, 1]
    k_array = db.get_material_k_numpy(page_id)[:, 1]

    return {
        "lambda": lambda_array * 1000,  # Convertir a nm
        "n": n_array,
        "k": k_array,
        "page_id": page_id,
        "page_name": nombre_pagina
    }





