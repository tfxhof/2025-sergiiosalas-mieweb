from abc import ABC, abstractmethod
from typing import List, Dict, Any


class IPresenter(ABC):


    @abstractmethod
    def mostrar_seleccion(self, event, page_selectors, plot, plot_option):
        """
        Maneja la selección y deselección de materiales, actualizando los selectores de páginas disponibles.
        """
        pass


    @abstractmethod
    def get_nombres_materiales(self):
        pass

    @abstractmethod
    def get_material_dict(self):
        pass

    @abstractmethod
    def get_material_data(self):
        pass


