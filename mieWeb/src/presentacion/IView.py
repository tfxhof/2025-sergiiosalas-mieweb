from abc import ABC, abstractmethod

class IView(ABC):

    @abstractmethod
    def actualizar_plot(self):
        """
        Updates the plot based on the selected options.
        """
        pass

    @abstractmethod
    def store_radius(self, event):
        """
        Displays an error message.
        """
        pass

    @abstractmethod
    def store_n_surrounding(self, event):
        """
        Displays an error message.
        """
        pass


    @abstractmethod
    def show(self):
        pass


    @abstractmethod
    def show_error(self, error_message):
        """
        Displays an error message.
        """
        pass

    @abstractmethod
    def manejar_seleccion(self, event):
        pass


