from refractivesqlite import dboperations as DB

# Ruta donde se guardará la base de datos SQLite
dbpath = "refractive.db"

# Crear un objeto para manejar la base de datos
db = DB.Database(dbpath)

# Descargar y crear la base de datos desde la URL predeterminada
db.create_database_from_url()

print(f"Base de datos creada y guardada en {dbpath}")


from refractivesqlite import dboperations as DB

dbpath = "refractive.db"
db = DB.Database(dbpath)

# Confirmar la URL desde donde se descargó la base de datos
db.check_url_version()
