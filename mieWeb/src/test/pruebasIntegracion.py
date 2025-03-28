import unittest
from unittest.mock import patch

from src.negocio.presenter import Presenter


class TestPresenterIntegration(unittest.TestCase):

    def setUp(self):
        # Instanciamos el Presenter para las pruebas
        self.presenter = Presenter()

    @patch('src.persistencia.acceso_datos.obtener_nombres_materiales')
    def test_obtener_nombres_materiales_integration(self, mock_obtener_nombres):
        # Configuramos el mock para que devuelva un valor esperado
        mock_obtener_nombres.return_value = (["Ag", "Au"], {"Material1": 1, "Material2": 2})

        # Ejecutamos la función del Presenter que llama al mock de acceso a datos
        nombres_materiales = self.presenter.get_nombres_materiales()

        # Verificamos que el mock se haya llamado correctamente
        mock_obtener_nombres.assert_called_once()

        # Verificamos que los valores obtenidos son correctos
        self.assertEqual(nombres_materiales, ["Material1", "Material2"])

    @patch('src.persistencia.acceso_datos.obtener_paginas_material')
    def test_obtener_opciones_paginas_integration(self, mock_obtener_paginas):
        # Configuramos el mock para que devuelva un valor esperado
        mock_obtener_paginas.return_value = [("Page1",), ("Page2",)]

        # Ejecutamos la función del Presenter que llama al mock de acceso a datos
        opciones = self.presenter.obtener_opciones_paginas("Material1")

        # Verificamos que el mock fue llamado correctamente con el argumento esperado
        mock_obtener_paginas.assert_called_once_with("Material1")

        # Verificamos que las opciones de páginas están en el formato esperado
        self.assertEqual(opciones, ['Select page', 'Page1', 'Page2'])

    @patch('src.persistencia.acceso_datos.obtener_datos_pagina')
    def test_obtener_valores_integration(self, mock_obtener_datos):
        # Configuramos el mock para que devuelva datos de ejemplo
        mock_obtener_datos.return_value = {
            "lambda": [500, 600],
            "n": [1.5, 1.6],
            "k": [0.02, 0.03],
            "page_id": 123,
            "page_name": "Page1"
        }

        # Ejecutamos la función del Presenter que llama al mock de acceso a datos
        self.presenter.obtener_valores("Material1", "Page1")

        # Verificamos que los datos se almacenaron correctamente en material_data
        self.assertIn("Material1", self.presenter.material_data)
        self.assertEqual(self.presenter.material_data["Material1"]["lambda"], [500, 600])
        self.assertEqual(self.presenter.material_data["Material1"]["n"], [1.5, 1.6])
        self.assertEqual(self.presenter.material_data["Material1"]["k"], [0.02, 0.03])

        # Verificamos que el mock se haya llamado correctamente
        mock_obtener_datos.assert_called_once_with("Material1", "Page1")
