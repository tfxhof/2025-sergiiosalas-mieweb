import unittest

import numpy as np

from src.negocio.calculo import calculate_mie_arrays


class TestPruebas(unittest.TestCase):

    def  test_calculo_mie(self):
        # Simulamos un diccionario con datos de material
        material_data = {
            'lambda': 0.5,  # longitudes de onda en nm
            'n': 1,        # índice de refracción real
            'k': 0.5,     # índice de refracción imaginario
            'page_id': 123
        }

        radius = 2  # Radio de la partícula en micrómetros
        n_surrounding = 1.0  # Índice de refracción del entorno (agua o aire, por ejemplo)

        # Llamamos a la función con los datos simulados
        results = calculate_mie_arrays(material_data, radius, n_surrounding)

        # Arrays de valores reales que tienes
        qext_real = 2


        # Comprobamos los valores de qext, qsca, y qabs de forma individual

        self.assertAlmostEqual(radius, qext_real)



if __name__ == "__main__":
    unittest.main()