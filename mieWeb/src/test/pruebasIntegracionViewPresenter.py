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










if __name__ == '__main__':
    unittest.main()

