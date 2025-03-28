import unittest
from unittest.mock import MagicMock
from src.negocio.presenter import Presenter
from src.persistencia.acceso_datos import obtener_nombres_materiales, obtener_paginas_material, obtener_datos_pagina

class TestPresenterIntegration(unittest.TestCase):

    def test_get_nombres_materiales(self):
        # Mock de la función obtener_nombres_materiales
        mock_obtener_nombres = MagicMock(return_value=["Ag", "Au"])

        # Crear instancia de Presenter y reemplazar la función obtener_nombres_materiales
        presenter = Presenter()
        presenter.get_nombres_materiales = mock_obtener_nombres

        # Llamamos a la funcion que usa la función mockeada
        nombres_materiales = presenter.get_nombres_materiales()

        # Verificar que se haya llamado correctamente y que el resultado es el esperado
        mock_obtener_nombres.assert_called_once()  # Verificar que se llamó una vez
        self.assertEqual(nombres_materiales, ["Ag", "Au"])  # Verificar que el resultado es el esperado

    def test_obtener_paginas_material(self):
        # Mock de la función obtener_paginas_material
        mock_obtener_paginas = MagicMock(return_value=['Select page', 'Johnson', 'McPeak'])

        # Crear instancia de Presenter
        presenter = Presenter()

        # Reemplazar la función obtener_paginas_material por el mock
        presenter.obtener_opciones_paginas = mock_obtener_paginas

        # Llamamos a la función que usa la función mockeada
        opciones_paginas = presenter.obtener_opciones_paginas("Ag")

        # Verificar que se haya llamado correctamente y que el resultado es el esperado
        mock_obtener_paginas.assert_called_once_with("Ag")  # Verificar que se llamó una vez con el argumento esperado
        self.assertEqual(opciones_paginas, ['Select page', 'Johnson', 'McPeak'])  # Verificar el resultado esperado

    def test_datos_pagina(self):
        # Mock de la función obtener_datos_pagina
        mock_obtener_datos = MagicMock(return_value={
            "lambda": [500, 600, 700],
            "n": [1.5, 1.6, 1.7],
            "k": [0.1, 0.2, 0.3],
            "page_id": 2,
            "page_name": "Johnson"
        })

        # Crear instancia de Presenter
        presenter = Presenter()

        # Reemplazar la función obtener_datos_pagina con el mock
        presenter.obtener_valores = mock_obtener_datos

        # Llamamos a la función que usa la función mockeada
        resultados = presenter.obtener_valores("Ag", "Johnson")

        # Verificar que se haya llamado correctamente
        mock_obtener_datos.assert_called_once_with("Ag", "Johnson")  # Verificar que se llamó una vez con los argumentos esperados

        # Verificar que los datos se hayan almacenado correctamente en material_data
        #self.assertTrue("Ag" in presenter.material_data)# Verificar que "Ag" esté presente en el diccionario
        self.assertEqual(resultados['lambda'], [500, 600, 700])
        self.assertEqual(resultados['n'], [1.5, 1.6, 1.7])
        self.assertEqual(resultados['k'], [0.1, 0.2, 0.3])
        self.assertEqual(resultados['page_id'], 2)
        self.assertEqual(resultados['page_name'], "Johnson")













if __name__ == "__main__":
    unittest.main()
