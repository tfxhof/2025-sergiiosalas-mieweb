import unittest
from unittest.mock import MagicMock

from numpy.ma.testutils import assert_equal

from src.negocio.presenter import Presenter
from src.presentacion.view import View


class TestActualizarPlot(unittest.TestCase):


    def test_view_calcular_grafica(self):

        # Configurar el mock para que calcular_datos_grafica devuelva datos de prueba
        mock_data = MagicMock(return_value=[("Ag", [1, 2, 3], [4, 5, 6])])

        presenter = Presenter()
        view = View(presenter)

        view.presenter.calcular_datos_grafica = mock_data  # Reemplazar la funcion con el mock

        # Llamar a la función que se está probando
        data_plot = view.presenter.calcular_datos_grafica()

        mock_data.assert_called_once()

        self.assertEqual(data_plot, [("Ag", [1, 2, 3], [4, 5, 6])])


    def test_store_radius(self):
        # Crear el mock para la vista
        mock_view = MagicMock()

        # Crear una instancia del presenter y pasar el mock de la vista
        presenter = Presenter()
        presenter.view = mock_view  # Asociar la vista mock al presenter

        # Crear la vista y pasar el presenter
        view = View(presenter)

        # Simular la entrada del radio con un valor de tipo float y convertirlo a string
        view.radius_input.value = str(50)
        view.store_radius(None)

        # Verificar que el valor se haya almacenado correctamente
        self.assertEqual(presenter.radius_value, 50)



    def test_store_n(self):
        # Crear el mock para la vista
        mock_view = MagicMock()

        # Crear una instancia del presenter y pasar el mock de la vista
        presenter = Presenter()
        presenter.view = mock_view  # Asociar la vista mock al presenter

        # Crear la vista y pasar el presenter
        view = View(presenter)

        # Simular la entrada del radio con un valor de tipo float y convertirlo a string
        view.n_surrounding_input.value = str(2)
        view.store_n_surrounding(None)

        # Verificar que el valor se haya almacenado correctamente
        self.assertEqual(presenter.n_surrounding_value, 2)



    def test_remove_from_material_data(self):
        # Crear el mock para la vista
        mock_view = MagicMock()

        # Crear una instancia del presenter y pasar el mock de la vista
        presenter = Presenter()
        presenter.view = mock_view

        # Crear la vista y pasar el presenter
        view = View(presenter)

        # Nombre de material a eliminar
        nombre_material = "Ag"


        # Asegurarse de que el material esté presente en la lista antes de eliminarlo
        presenter.material_data = ["Ag", "Cu", "Fe"]

        # Verificar que el material esté en la lista antes de eliminarlo
        self.assertIn(nombre_material, presenter.material_data)

        view.presenter.remove_from_material_data(0)

        # Verificar que el material se haya eliminado correctamente
        self.assertNotIn("Ag", presenter.material_data)



    def test_obtener_opciones_paginas(self):

        # Crear una instancia del presenter y pasar el mock de la vista
        presenter = Presenter()

        # Crear la vista y pasar el presenter
        view = View(presenter)

        presenter.view = view

        # Nombre del material a obtener las opciones de páginas
        nombre_material = "Ag"

        # Simular la función que obtiene las opciones de páginas
        view.presenter.obtener_opciones_paginas = MagicMock(return_value=["Select page", "Johnson", "McPeak"])

        # Llamar a la función que se está probando
        opciones_paginas = view.presenter.obtener_opciones_paginas(nombre_material)

        # Verificar que se haya llamado correctamente y que el resultado sea el esperado
        view.presenter.obtener_opciones_paginas.assert_called_once_with(nombre_material)
        self.assertEqual(opciones_paginas, ["Select page", "Johnson", "McPeak"])





    def test_obtener_valores(self):
        # Crear una instancia del presenter y pasar el mock de la vista
        presenter = Presenter()

        # Crear la vista y pasar el presenter
        view = View(presenter)

        presenter.view = view

        # Simular los datos de la página
        mock_data = {
            "lambda": [500, 600, 700],
            "n": [1.5, 1.6, 1.7],
            "k": [0.1, 0.2, 0.3],
            "page_id": 2,
            "page_name": "Johnson"
        }

        # Reemplazar la función obtener_datos_pagina con el mock
        view.presenter.obtener_valores = MagicMock(return_value=mock_data)

        # Llamar a la función que se está probando
        resultados = view.presenter.obtener_valores("Ag", "Johnson")

        # Verificar que se haya llamado correctamente
        view.presenter.obtener_valores.assert_called_once_with("Ag", "Johnson")

        # Verificar que los datos se hayan almacenado correctamente en material_data
        self.assertEqual(resultados['lambda'], [500, 600, 700])
        self.assertEqual(resultados['n'], [1.5, 1.6, 1.7])
        self.assertEqual(resultados['k'], [0.1, 0.2, 0.3])



if __name__ == '__main__':
    unittest.main()

