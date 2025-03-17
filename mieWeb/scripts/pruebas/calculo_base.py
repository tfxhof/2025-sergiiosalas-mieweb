import numpy as np
from miepython import miepython

lamb = 0.5 # Valores de qext
n = 1  # Valores de qsca
k = 0.5  # Valores de qabs

    #Calculate the complex refractive index m and the size parameter x
m = (n - 1.0j * k)
x = 2 * np.pi

    # Calculate the Mie scattering parameters using miepython
qext, qsca, qback, g = miepython.mie(m, x)

# Absorption coefficient
qabs = qext - qsca

# Store results in the dictionary
results = {
        'qext': qext,
        'qsca': qsca,
        'qabs': qabs,
    }

print(results)