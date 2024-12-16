import sqlite3
from refractivesqlite import dboperations as DB

# Ruta a la base de datos
db_path = r'C:\Users\sersa\Desktop\UC\tfg\tfg\mieWeb\refractive2.db'

# Conexión a la base de datos
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Inicializar el objeto DB
db = DB.Database(db_path)

# Obtener todas las páginas de la base de datos
cursor.execute("SELECT pageid FROM pages")
page_ids = cursor.fetchall()

# Recorrer todas las páginas y eliminar las que no tienen valores válidos de n o k
for pageid_tuple in page_ids:
    pageid = pageid_tuple[0]

    # Obtener los valores de n y k
    n_values = db.get_material_n_numpy(pageid)
    k_values = db.get_material_k_numpy(pageid)

    # Si no hay valores de n o k, eliminar la página de la base de datos
    if n_values is None or k_values is None or len(n_values) == 0 or len(k_values) == 0:
        print(f"Eliminando página con pageid {pageid} porque no tiene valores de n o k válidos.")

        # Eliminar la página de la base de datos
        cursor.execute("DELETE FROM pages WHERE pageid = ?", (pageid,))
        conn.commit()

# Cerrar la conexión
conn.close()
