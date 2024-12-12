import numpy as np
import miepython
import sqlite3

def calculate_mie_array(valor_lambda_array, n_array, k_array, radius):
    qext_array = []
    qsca_array = []
    qabs_array = []

    for valor_lambda, n, k in zip(valor_lambda_array, n_array, k_array):
        # Calculo M
        m = n_array - 1.0j * k_array

        # x = 2piR / lambda
        x = 2 * np.pi * radius / valor_lambda_array

        # Calcular los parámetros usando la función de miepython
        qext, qsca, qback, g = miepython.mie(m, x)

        # qabs
        qabs = qext - qsca

        qext_array.append(qext)
        qsca_array.append(qsca)
        qabs_array.append(qabs)

    return np.array(qext_array), np.array(qsca_array), np.array(qabs_array)

# Conectar a la base de datos SQLite
db_path = r"C:\Users\sersa\Desktop\UC\tfg\tfg\prueba.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# ID del material que queremos filtrar
material_id = 1

# Leer los datos de la base de datos filtrando por el ID del material
cursor.execute("SELECT longitud_onda, n, k FROM DatosDeRefraccion WHERE material_id = ?", (material_id,))
data = cursor.fetchall()

# Cerrar la conexión a la base de datos
conn.close()

# Convertir los datos leídos en arrays de numpy
valor_lambda_array = np.array([row[0] for row in data])
n_array = np.array([row[1] for row in data])
k_array = np.array([row[2] for row in data])
radius = 0.1  # Valor concreto del radio de las partículas

# Llamada a la función con los parámetros leídos de la base de datos
qext_array, qsca_array, qabs_array = calculate_mie_array(valor_lambda_array, n_array, k_array, radius)

# Imprimir los resultados
for i in range(len(valor_lambda_array)):
    print(f"Para λ = {valor_lambda_array[i]:.2f} μm, n = {n_array[i]:.2f}, k = {k_array[i]:.2f}, radio = {radius:.2f} μm:")
    print(f"  Coeficiente de extinción (qext): {qext_array[i]:.4f}")
    print(f"  Coeficiente de dispersión (qsca): {qsca_array[i]:.4f}")
    print(f"  Coeficiente de absorción (qabs): {qabs_array[i]:.4f}")