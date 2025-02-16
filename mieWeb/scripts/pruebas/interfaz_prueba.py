import sqlite3
import panel as pn

# Inicializar Panel
pn.extension()

# Función para conectar a la base de datos y obtener los materiales
def obtener_materiales(busqueda=None):
    conn = sqlite3.connect(r"C:\Users\sersa\Desktop\UC\tfg\tfg\mieWeb\pruebas\prueba.db")  # Cambia esto a la ruta de tu base de datos
    cursor = conn.cursor()

    if busqueda:
        # Consultar los materiales que coinciden exactamente con la búsqueda (ignorando mayúsculas/minúsculas)
        cursor.execute("SELECT id, nombre FROM Material WHERE LOWER(nombre) = LOWER(?)", (busqueda,))
    else:
        # Consultar todos los materiales
        cursor.execute("SELECT id, nombre FROM Material")

    # Obtener todos los resultados
    materiales = cursor.fetchall()

    conn.close()

    return materiales

# Obtener los materiales de la base de datos
materiales = obtener_materiales()

# Crear una lista con los nombres de los materiales para el multi-choice
material_names = [material[1] for material in materiales]
material_dict = {material[1]: material[0] for material in materiales}  # Diccionario de {nombre: id}

# Crear un widget de multi-choice (selección múltiple)
multi_choice = pn.widgets.MultiChoice(name="Seleccionar Materiales", options=material_names, width=400, placeholder="Seleccione los materiales que desee")

# Función que se ejecuta cuando el usuario selecciona materiales
def mostrar_seleccion(event):
    # Obtener los materiales seleccionados
    seleccionados = event.new
    ids_seleccionados = [material_dict[nombre] for nombre in seleccionados]  # Convertir nombres seleccionados a IDs
    print(f"Materiales seleccionados: {seleccionados}, IDs: {ids_seleccionados}")

    # Aquí puedes hacer cualquier cosa con los materiales seleccionados (e.g., cálculos)

# Conectar la función de selección a los multi-choice
multi_choice.param.watch(mostrar_seleccion, 'value')

# Mostrar los widgets
pn.Column(multi_choice).show()
