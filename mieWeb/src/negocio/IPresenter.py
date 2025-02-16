from abc import ABC, abstractmethod
from typing import List, Dict, Any


class IPresenter(ABC):

    # Variables requeridas que deben estar disponibles para la View
    nombres_materiales: List[str]
    material_dict: Dict[str, Any]
    material_data: Dict[str, Dict[str, Any]]

    @abstractmethod
    def mostrar_seleccion(self, event, page_selectors, plot, plot_option):
        """
        Maneja la selección y deselección de materiales, actualizando los selectores de páginas disponibles.
        """
        pass

    @abstractmethod
    def actualizar_valores(self, event, nombre):
        """
        Carga los valores de la base de datos cuando el usuario selecciona una página.
        """
        pass


