import unittest
import numpy as np
import csv
import os


from src.negocio.calculo import calculate_mie_arrays
from src.persistencia.acceso_datos import obtener_datos_pagina


class TestPruebas(unittest.TestCase):


    def read_tsv(self, file_name):

        base_dir = os.path.dirname(os.path.abspath(__file__))  # Carpeta 'test'
        file_path = os.path.join(base_dir, "..", "datos", file_name)  # Subir un nivel y entrar en 'datos'

        data = {
            "Lambda": [],
            "Qext": [],
            "Qsca": [],
            "Qabs": []
        }

        with open(file_path, mode='r') as file:
            reader = csv.reader(file, delimiter='\t')

            for row in reader:
                data["Lambda"].append(float(row[0]))
                data["Qext"].append(float(row[1]))
                data["Qsca"].append(float(row[2]))
                data["Qabs"].append(float(row[3]))

        return data


    # Pruebas unitarias para el cálculo de Mie
    def  test_calculo_mie_1(self):

        material_1 = obtener_datos_pagina("Ag", "Johnson")
        radius = 25  # Radio de la partícula en micrómetros
        n_surrounding = 1.0  # Índice de refracción del entorno (agua o aire, por ejemplo)

        results_material = calculate_mie_arrays(material_1, radius, n_surrounding)


        file_name = 'Q_Ag_Johnson_R_25_nmed_1.txt'
        real_data = self.read_tsv(file_name)

        for real_value, calc_value in zip(real_data["Qext"], results_material["qext"]):
            self.assertAlmostEqual(real_value, calc_value, delta=0.001)

        for real_value, calc_value in zip(real_data["Qabs"], results_material["qabs"]):
            self.assertAlmostEqual(real_value, calc_value, delta=0.001)

        for real_value, calc_value in zip(real_data["Qsca"], results_material["qsca"]):
            self.assertAlmostEqual(real_value, calc_value, delta=0.001)



    def  test_calculo_mie_2(self):

        material_2 = obtener_datos_pagina("Ag", "Johnson")
        radius = 50  # Radio de la partícula en micrómetros
        n_surrounding = 1.0  # Índice de refracción del entorno (agua o aire, por ejemplo)

        results_material = calculate_mie_arrays(material_2, radius, n_surrounding)


        file_name = 'Q_Ag_Johnson_R_50_nmed_1.txt'
        real_data = self.read_tsv(file_name)

        for real_value, calc_value in zip(real_data["Qext"], results_material["qext"]):
            self.assertAlmostEqual(real_value, calc_value, delta=0.001)

        for real_value, calc_value in zip(real_data["Qabs"], results_material["qabs"]):
            self.assertAlmostEqual(real_value, calc_value, delta=0.001)

        for real_value, calc_value in zip(real_data["Qsca"], results_material["qsca"]):
            self.assertAlmostEqual(real_value, calc_value, delta=0.001)

    def  test_calculo_mie_3(self):

        material_3 = obtener_datos_pagina("Au", "Johnson")
        radius = 50  # Radio de la partícula en micrómetros
        n_surrounding = 1.5  # Índice de refracción del entorno (agua o aire, por ejemplo)

        results_material = calculate_mie_arrays(material_3, radius, n_surrounding)


        file_name = 'Q_Au_Johnson_R_50_nmed_1.5.txt'
        real_data = self.read_tsv(file_name)

        for real_value, calc_value in zip(real_data["Qext"], results_material["qext"]):
            self.assertAlmostEqual(real_value, calc_value, delta=0.001)

        for real_value, calc_value in zip(real_data["Qabs"], results_material["qabs"]):
            self.assertAlmostEqual(real_value, calc_value, delta=0.001)

        for real_value, calc_value in zip(real_data["Qsca"], results_material["qsca"]):
            self.assertAlmostEqual(real_value, calc_value, delta=0.001)


    def  test_calculo_mie_4(self):

        material_4 = obtener_datos_pagina("Au", "Johnson")
        radius = 50  # Radio de la partícula en micrómetros
        n_surrounding = 1.0  # Índice de refracción del entorno (agua o aire, por ejemplo)

        results_material = calculate_mie_arrays(material_4, radius, n_surrounding)


        file_name = 'Q_Au_Johnson_R_50_nmed_1.txt'
        real_data = self.read_tsv(file_name)

        for real_value, calc_value in zip(real_data["Qext"], results_material["qext"]):
            self.assertAlmostEqual(real_value, calc_value, delta=0.001)

        for real_value, calc_value in zip(real_data["Qabs"], results_material["qabs"]):
            self.assertAlmostEqual(real_value, calc_value, delta=0.001)

        for real_value, calc_value in zip(real_data["Qsca"], results_material["qsca"]):
            self.assertAlmostEqual(real_value, calc_value, delta=0.001)



    def  test_calculo_mie_5(self):

        material_5 = obtener_datos_pagina("Au", "Johnson")
        radius = 100  # Radio de la partícula en micrómetros
        n_surrounding = 1.0  # Índice de refracción del entorno (agua o aire, por ejemplo)

        results_material = calculate_mie_arrays(material_5, radius, n_surrounding)


        file_name = 'Q_Au_Johnson_R_100_nmed_1.txt'
        real_data = self.read_tsv(file_name)

        for real_value, calc_value in zip(real_data["Qext"], results_material["qext"]):
            self.assertAlmostEqual(real_value, calc_value, delta=0.001)

        for real_value, calc_value in zip(real_data["Qabs"], results_material["qabs"]):
            self.assertAlmostEqual(real_value, calc_value, delta=0.001)

        for real_value, calc_value in zip(real_data["Qsca"], results_material["qsca"]):
            self.assertAlmostEqual(real_value, calc_value, delta=0.001)


if __name__ == "__main__":
    unittest.main()
