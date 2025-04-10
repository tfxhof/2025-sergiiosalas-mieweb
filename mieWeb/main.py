from src.negocio.presenter import Presenter
from src.presentacion.view import View



presenter = Presenter()
view = View(presenter)

presenter.view = view

view.show()



