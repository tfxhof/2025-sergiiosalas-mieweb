import os
import yaml
import sqlite3

# Conectar a la base de datos SQLite
db_path = r"C:\Users\sersa\Desktop\UC\tfg\tfg\materials.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()


# Cargar el contenido del archivo YAML en la variable library
yaml_file_path = r"C:\Users\sersa\Desktop\UC\tfg\tfg\refractiveindex.info-database\database\catalog-nk.yml"
with open(yaml_file_path, 'r') as file:
    library = yaml.safe_load(file)

def UpdateBookList():
    for material_name in library:
        if "content" in material_name:
            for item in material_name["content"]:
                if "BOOK" in item:
                    book_name = item.get("BOOK")
                    # Insertar el nombre del material en la base de datos
                    cursor.execute("INSERT OR IGNORE INTO Material (nombre) VALUES (?)", (book_name,))
    # Guardar los cambios en la base de datos
    conn.commit()

# Llamar a la función para actualizar la lista de estantes y guardar los nombres en la base de datos
UpdateBookList()

# Cerrar la conexión a la base de datos
conn.close()