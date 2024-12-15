import numpy as np
import miepython
from Interfaz import material_data  # Import the material data from Interfaz

def calculate_mie_arrays_single(page_id, radius):
    valor_lambda_array, n_array, k_array = material_data[page_id]

    # Calculo del índice complejo m y el parámetro x
    m = n_array - 1.0j * k_array
    x = 2 * np.pi * radius / valor_lambda_array

    # Calcular los parámetros usando la función de miepython
    qext, qsca, qback, g = miepython.mie(m, x)

    # Coeficiente de absorción
    qabs = qext - qsca

    return qext, qsca, qabs

# Ejemplo de uso
material_id = 1  # ID del material
radius = 0.1  # Radio de las partículas en micrómetros

# Llamada a la función con los parámetros leídos de Interfaz
qext, qsca, qabs = calculate_mie_arrays_single(material_id, radius)