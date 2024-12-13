import numpy as np
import miepython
import sqlite3

def calculate_mie_arrays(material_data, radius):
    """
    Calcula los coeficientes de extinción, dispersión y absorción para varios materiales.

    Args:
        material_data (dict): Diccionario donde las claves son los IDs de materiales y los valores son tuplas de arrays (lambda, n, k).
        radius (float): Radio de las partículas en micrómetros.

    Returns:
        dict: Diccionario con los resultados por material, donde cada clave es un ID de material y el valor es una tupla de arrays (qext, qsca, qabs).
    """
    results = {}
    for material_id, (valor_lambda_array, n_array, k_array) in material_data.items():
        # Calculo del índice complejo m y el parámetro x
        m = n_array - 1.0j * k_array
        x = 2 * np.pi * radius / valor_lambda_array

        # Calcular los parámetros usando la función de miepython
        qext, qsca, qback, g = miepython.mie(m, x)

        # Coeficiente de absorción
        qabs = qext - qsca

        # Guardar resultados en el diccionario
        results[material_id] = (qext, qsca, qabs)

    return results

# Conectar a la base de datos SQLite
db_path = r"C:\Users\sersa\Desktop\UC\tfg\tfg\mieWeb\pruebas\prueba.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# IDs de los materiales que queremos filtrar
material_ids = [1, 2,3,4]  # Lista de IDs de materiales

# Leer los datos de la base de datos para cada material
material_data = {}
for material_id in material_ids:
    cursor.execute("SELECT longitud_onda, n, k FROM DatosDeRefraccion WHERE material_id = ?", (material_id,))
    data = cursor.fetchall()
    if data:
        # Convertir los datos leídos en arrays de numpy
        valor_lambda_array = np.array([row[0] for row in data])
        n_array = np.array([row[1] for row in data])
        k_array = np.array([row[2] for row in data])
        material_data[material_id] = (valor_lambda_array, n_array, k_array)

# Cerrar la conexión a la base de datos
conn.close()

# Valor del radio de las partículas
radius = 0.1  # En micrómetros

# Llamada a la función con los parámetros leídos de la base de datos
results = calculate_mie_arrays(material_data, radius)

# Imprimir los resultados para comprobar
for material_id, (qext_array, qsca_array, qabs_array) in results.items():
    print(f"Resultados para el material ID {material_id}:")
    valor_lambda_array, n_array, k_array = material_data[material_id]
    for i in range(len(valor_lambda_array)):
        print(f"  Para λ = {valor_lambda_array[i]:.2f} μm, n = {n_array[i]:.2f}, k = {k_array[i]:.2f}, radio = {radius:.2f} μm:")
        print(f"    Coeficiente de extinción (qext): {qext_array[i]:.4f}")
        print(f"    Coeficiente de dispersión (qsca): {qsca_array[i]:.4f}")
        print(f"    Coeficiente de absorción (qabs): {qabs_array[i]:.4f}")

# Ejemplo: ahora puedes usar los resultados para gráficas en matplotlib
