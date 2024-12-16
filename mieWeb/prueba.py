import sqlite3
from refractivesqlite import dboperations as DB

# Ruta a la base de datos
db_path = r'C:\Users\sersa\Desktop\UC\tfg\tfg\mieWeb\refractive.db'

# Crear una instancia de la base de datos
db = DB.Database(db_path)

# Obtener los datos del índice de refracción para el material con pageid 255
material_n_data = db.get_material_k_numpy(103)

# Imprimir los datos obtenidos
print(material_n_data)