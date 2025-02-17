from src.negocio.presenter import Presenter
from src.presentacion.view import View


def main():

    presenter = Presenter()
    view = View(presenter)

    presenter.View = view
    view.Presenter = presenter

    view.show()

    if __name__=="__main__":
        main()

