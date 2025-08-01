import numpy as np
import miepython

def calculate_mie_arrays(material_data, radius, n_surrounding):
    results = {}

    # Extract lambda, n, and k arrays from material_data
    lambda_array = material_data['lambda']  # Convert to nm
    n_array = material_data['n']
    k_array = material_data['k']

    # Calculate the complex refractive index m and the size parameter x
    m = (n_array - 1.0j * k_array) / n_surrounding
    x = 2 * np.pi * radius * n_surrounding/ lambda_array

    # Calculate the Mie scattering parameters using miepython
    qext, qsca, qback, g = miepython.mie(m, x)

    # Absorption coefficient
    qabs = qext - qsca

    # Store results in the dictionary
    results = {
        'qext': qext,
        'qsca': qsca,
        'qabs': qabs,
        'page_id': material_data['page_id']
    }

    return results