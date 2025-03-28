from src.negocio import calculo
from src.persistencia.acceso_datos import obtener_nombres_materiales, obtener_paginas_material, obtener_datos_pagina
from src.negocio.IPresenter import IPresenter
from src.presentacion.IView import IView
from src.persistencia.acceso_datos import db_path


class Presenter(IPresenter):
    def __init__(self, radius_value = None, n_surrounding_value = None):
        self.view: IView = None
        self.radius_value = radius_value
        self.n_surrounding_value = n_surrounding_value
        self.valid_radius = False
        self.valid_n_surrounding = False

        # Obtener los nombres de los materiales y el diccionario de materiales
        self.nombres_materiales = []

        # Diccionario para almacenar los valores de lambda, n y k para cada página
        self.material_data = {}

        self.db_path = db_path

    def update_n_surrounding(self, n):
        self.n_surrounding_value = n

    def update_radius(self, radius):
        self.radius_value = radius

    def get_nombres_materiales(self):
        self.nombres_materiales = obtener_nombres_materiales()
        return self.nombres_materiales

    def get_material_data(self):
        return self.material_data

    def get_n_surrounding_value(self):
        return self.n_surrounding_value

    def get_radius_value(self):
        return self.radius_value



    def remove_from_material_data(self, nombre):
        self.material_data.pop(nombre)


    def obtener_opciones_paginas(self, nombre):
        paginas = obtener_paginas_material(nombre)
        opciones_paginas = ['Select page'] + [pagina[0] for pagina in paginas]
        return opciones_paginas


    def obtener_valores (self, nombre, page_name):
        try:
            resultados = obtener_datos_pagina(nombre, page_name)

            lambda_array = resultados["lambda"]
            n_array = resultados["n"]
            k_array = resultados["k"]
            page_id = resultados["page_id"]

            self.material_data[nombre] = {
                'lambda': lambda_array,
                'n': n_array,
                'k': k_array,
                'page_id': page_id,
                'page_name': page_name
            }
        except Exception as e:
            self.view.show_error(f"Error: {str(e)}")

    def calcular_datos_grafica(self, plot_option):
        # Validar que los valores no sean None o cadenas vacías
        if not self.radius_value or not self.n_surrounding_value:
            return None

        try:
            radius = float(self.radius_value)
            n_surrounding = float(self.n_surrounding_value)
            if radius <= 0 or n_surrounding <= 0:
                return None
        except ValueError:
            return None  # Si hay un error de conversión, retornamos None

        data_plot = []

        for material_name, data in self.material_data.items():
            results = calculo.calculate_mie_arrays(data, radius, n_surrounding)
            x = data['lambda']
            y = results[plot_option]
            data_plot.append((material_name, x, y))  # Solo devolver los datos puros

        return data_plot

    def radius_store(self, radius):
        try:
            r = float(radius)
            if r <= 0:
                raise ValueError("Radius value must be greater than 0")

            # Si el valor es válido, lo almacenamos
            self.update_radius(r)
            self.valid_radius = True
            self.view.show_error("")  # Limpiar mensaje de error

            # Solo actualizamos la gráfica si ambos valores son válidos
            if self.valid_n_surrounding:
                self.view.actualizar_plot()

            else:
                self.view.show_error("Enter a valid value for the refractive index of the medium")

        except ValueError:
            # Almacenamos el valor inválido para el radio
            self.update_radius(radius)
            self.valid_radius = False
            self.view.show_error("Error: Enter a valid value for radius")


    def n_surrounding_store(self, n_surrounding):
        try:
            n = float(n_surrounding)
            if n <= 0:
                raise ValueError("The value of the refractive index of the medium must be greater than 0")

            # Si el valor es válido, lo almacenamos
            self.update_n_surrounding(n)
            self.valid_n_surrounding = True
            self.view.show_error("")  # Limpiar mensaje de error

            # Solo actualizamos la gráfica si ambos valores son válidos
            if self.valid_radius:
                self.view.actualizar_plot()
            else:
                self.view.show_error("Enter a valid value for radius")


        except ValueError:
            # Almacenamos el valor inválido para el índice de refracción
            self.update_n_surrounding(n_surrounding)
            self.valid_n_surrounding = False
            self.view.show_error("Error: Enter a valid value for the refractive index of the medium")
