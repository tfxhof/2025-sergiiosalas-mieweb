import os
import sqlite3

import panel as pn
from bokeh.models import LegendItem
from bokeh.palettes import Category10
from numba import none

# Import the function from AccesoDatos.py
from refractivesqlite import dboperations as DB
from src.negocio import calculo
from src.persistencia.acceso_datos import obtener_nombres_materiales, obtener_paginas_material, obtener_datos_pagina
from src.negocio.IPresenter import IPresenter
from src.presentacion.IView import IView
from src.persistencia.acceso_datos import db_path


class Presenter(IPresenter):
    def __init__(self, radius_value = None, n_surrounding_value = 1.0):
        self.view = None
        self.radius_value = radius_value
        self.n_surrounding_value = n_surrounding_value

        # Obtener los nombres de los materiales y el diccionario de materiales
        self.nombres_materiales, self.material_dict = obtener_nombres_materiales()

        # Diccionario para almacenar los valores de lambda, n y k para cada página
        self.material_data = {}

        # Mensaje de error
        self.error_message = pn.pane.Markdown("", sizing_mode="stretch_width")

        self.db_path = db_path

    def update_n_surrounding(self, n):
        self.n_surrounding_value = n

    def update_radius(self, radius):
        self.radius_value = radius

    def get_nombres_materiales(self):
        return self.nombres_materiales

    def get_material_dict(self):
        return self.material_dict

    def get_material_data(self):
        return self.material_data

    def get_n_surrounding_value(self):
        return self.n_surrounding_value

    def get_radius_value(self):
        return self.radius_value




    # Función que se ejecuta cuando el usuario selecciona materiales
    def mostrar_seleccion(self, event, page_selectors,plot, plot_option):
        seleccionados = set(event.new)
        for widget in list(page_selectors):
            nombre_material = widget.name.split(" for ")[1]
            if nombre_material not in seleccionados:  # Si el material fue deseleccionado
                page_selectors.remove(widget)  # Eliminar el selector de página
                self.material_data.pop(nombre_material, None)  # Eliminar el material de `material_data`

        for nombre in seleccionados:
            if not any(widget.name.split(" for ")[1] == nombre for widget in page_selectors):

                paginas = obtener_paginas_material(nombre)

                opciones_paginas = ['Select page'] + [pagina[0] for pagina in paginas]
                page_selector = pn.widgets.Select(
                    name=f"Select page for {nombre}",
                    options=opciones_paginas,
                    value='Select page',
                    width=200
                )
                page_selectors.append(page_selector)

                def actualizar_valores(event, nombre=nombre):
                    if event.new == 'Select page':
                        self.material_data.pop(nombre, None)
                    else:
                        page_name = event.new
                        try:
                            resultados = obtener_datos_pagina(nombre, page_name)

                            lambda_array = resultados["lambda"]
                            n_array = resultados["n"]
                            k_array = resultados["k"]
                            page_id = resultados["page_id"]

                            self.material_data[nombre] = {
                                'lambda': lambda_array * 1000,  # Convertir a nm
                                'n': n_array,
                                'k': k_array,
                                'page_id': page_id,
                                'page_name': page_name
                            }
                        except Exception as e:
                            self.error_message.object = f"Error: {str(e)}"
                    self.view.actualizar_plot()

                page_selector.param.watch(actualizar_valores, 'value')
        self.view.actualizar_plot()



    def calcular_datos_grafica (self, plot_option):

        if self.radius_value is None:
            return None

        colors = Category10[10]  # Use a color palette with 10 colors
        color_index = 0
        legend_items = []
        data_plot = []

        for material_name, data in self.material_data.items():
            results = calculo.calculate_mie_arrays(
                data, float(self.radius_value), float(self.n_surrounding_value)
            )
            x = data['lambda']
            y = results[plot_option]
            color = colors[color_index % len(colors)]  # Ciclo de colores
            legend_item = LegendItem(label=f'{plot_option} {material_name}', renderers=[])
            data_plot.append((x, y, color, legend_item))
            color_index += 1

        return data_plot, legend_items











