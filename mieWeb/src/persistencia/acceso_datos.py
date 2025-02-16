import sqlite3
from refractivesqlite import dboperations as DB

# Ruta a la base de datos
db_path = './refractive.db'

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