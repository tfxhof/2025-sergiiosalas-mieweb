from abc import ABC, abstractmethod
from typing import List, Dict, Any


class IPresenter(ABC):

    @abstractmethod
    def update_n_surrounding(self, n):
        pass

    @abstractmethod
    def update_radius(self, radius):
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

    @abstractmethod
    def get_n_surrounding_value(self):
        pass

    @abstractmethod
    def get_radius_value(self):
        pass

    @abstractmethod
    def mostrar_seleccion(self, event, page_selectors, plot, plot_option):
        pass

    @abstractmethod
    def calcular_datos_grafica(self, plot_option):
        pass

    @abstractmethod
    def radius_store (self, radius):
        pass

    @abstractmethod
    def n_surrounding_store (self, n_surrounding):
        pass
