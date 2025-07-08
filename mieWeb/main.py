from src.negocio.presenter import Presenter
from src.presentacion.view import View

default_radius_value = 50
default_n_surrounding_value = 1

presenter = Presenter(default_radius_value, default_n_surrounding_value)

view = View(presenter)

presenter.view = view

view.show()
