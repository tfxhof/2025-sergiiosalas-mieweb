import os
import sqlite3

import panel as pn
from numba import none

# Import the function from AccesoDatos.py
from refractivesqlite import dboperations as DB
from src.persistencia.acceso_datos import obtener_nombres_materiales
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
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT pageid, page FROM pages WHERE book = ?", (nombre,))
                paginas = cursor.fetchall()
                conn.close()
                opciones_paginas = ['Select page'] + [pagina[1] for pagina in paginas]
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
                            conn = sqlite3.connect(self.db_path)
                            cursor = conn.cursor()
                            cursor.execute("SELECT pageid FROM pages WHERE page = ? AND book = ?", (page_name, nombre))
                            page_id = cursor.fetchone()[0]
                            conn.close()
                            db = DB.Database(self.db_path)
                            lambda_array = db.get_material_n_numpy(page_id)[:, 0]
                            n_array = db.get_material_n_numpy(page_id)[:, 1]
                            k_array = db.get_material_k_numpy(page_id)[:, 1]
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
















