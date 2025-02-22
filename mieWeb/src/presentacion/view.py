import io
import sqlite3
import panel as pn
from bokeh.plotting import figure
from bokeh.models import HoverTool, LegendItem, canvas
from bokeh.io import output_notebook, export, export_svg


from bokeh.palettes import Category10
from bokeh.models import Legend
from bokeh.io.export import export_svgs
from bokeh.plotting import figure, output_file, save
import chromedriver_autoinstaller
from bokeh.io.export import export_svgs
from selenium import webdriver
import tempfile
import zipfile

from refractivesqlite import dboperations as DB


from src.negocio.IPresenter import IPresenter
from src.negocio.presenter import Presenter
from src.presentacion.IView import IView
from src.negocio import calculo, descarga

class View(IView):
    def __init__(self, presenter):
        self.presenter = presenter  # Se guarda la instancia de Presenter

        # Mensaje de error
        self.error_message = pn.pane.Markdown("", sizing_mode="stretch_width")

        # Crear un widget de selección múltiple con Panel
        self.multi_choice = pn.widgets.MultiChoice(
            name="Select materials",
            options= self.presenter.get_nombres_materiales(),
            width=350,
            placeholder="Select the materials you wish to compare"
        )

        # Contenedor para los widgets de selección de páginas
        self.page_selectors = pn.Column(sizing_mode="stretch_width")

        # Mensaje de error
        self.error_message = pn.pane.Markdown("", sizing_mode="stretch_width")

        # Initialize Bokeh output
        output_notebook()

        # Create a Bokeh figure with fixed dimensions
        self.plot = figure(
            x_axis_label='Wavelength (nm)',
            y_axis_label='qext',
            tools="pan,box_zoom,reset,hover",
            tooltips=[("Wavelength", "@x"), ("Value", "@y")],
            width=500,  # Fixed width
            height=500  # Fixed height
        )

        # Crear el contenedor para la gráfica sin leyenda
        self.plot_pane = pn.pane.Bokeh(self.plot, sizing_mode="stretch_both", min_height=400, min_width=400, max_height=50,
                                  max_width=500)

        # Añadimos un RadioButtonGroup para seleccionar qué graficar
        self.plot_option = pn.widgets.RadioBoxGroup(
            name='Select metric to plot',
            options=['qext', 'qsca', 'qabs'],
            value='qext',  # Valor predeterminado
            inline=True
        )

        # Conectar el RadioButtonGroup para actualizar la gráfica cuando se cambie la opción
        self.plot_option.param.watch(lambda event: self.actualizar_plot(), 'value')

        # Conectar la función mostrar_seleccion al multi-choice
        self.multi_choice.param.watch(
            lambda event: self.presenter.mostrar_seleccion(event, self.page_selectors, self.plot, self.plot_option), 'value')


        # Crear una entrada de texto para el radio
        self.radius_input = pn.widgets.TextInput(
            name='Radius (nm)',
            placeholder='Enter the radius value in nanometers',
            width=300
        )

        # Botón para confirmar el radio
        self.confirm_radius_button = pn.widgets.Button(
            name='Confirm radius',
            button_type='primary',
            width=50
        )

        # Adjuntar la función store_radius al evento del botón
        self.confirm_radius_button.on_click(self.store_radius)

        # Crear una entrada de texto para el n del medio
        self.n_surrounding_input = pn.widgets.TextInput(
            name='Refractive index of the medium',
            placeholder='Enter value',
            value='1',  # Valor predeterminado
            width=300
        )

        # Botón para confirmar el n del medio
        self.confirm_n_surrounding_button = pn.widgets.Button(
            name='Confirm value',
            button_type='primary',
            width=50
        )

        # Adjuntar la función store_n_surrounding al evento del botón
        self.confirm_n_surrounding_button.on_click(self.store_n_surrounding)

        # Crear un botón para descargar la gráfica como PDF
        self.download_button_pdf = pn.widgets.Button(
            name="Download as PDF",
            button_type="primary",
            width=200
        )

        self.download_button_txt = pn.widgets.FileDownload(
            button_type='primary',
            callback=lambda: descarga.descargar_txt(self.presenter),
            filename="materials.zip"
        )

        # Inicializar la gráfica
        self.actualizar_plot()




    def show(self):

        # Actualizar el layout para incluir el RadioButtonGroup encima de la gráfica
        layout = pn.Row(
            # Columna izquierda: Selector de materiales y páginas
            pn.Column(
                self.multi_choice,  # Selector de materiales
                self.page_selectors,  # Selectores de páginas dinámicos
                width=400  # Ancho fijo para esta columna
            ),
            # Columna central: Radio, gráfica y botón de descarga
            pn.Column(
                pn.Row(
                    self.radius_input,  # Entrada para el radio
                    pn.Column(  # Usamos un Column para aplicar un espaciado
                        self.confirm_radius_button,  # Botón para confirmar el radio
                        sizing_mode='fixed',  # Tamaño fijo para que el botón no estire
                        margin=(16, 0, 0, 0)  # Eliminar márgenes adicionales
                    ),
                ),
                pn.Row(
                    self.n_surrounding_input,  # Entrada para el n del medio
                    pn.Column(  # Usamos un Column para aplicar un espaciado
                        self.confirm_n_surrounding_button,  # Botón para confirmar el n del medio
                        sizing_mode='fixed',  # Tamaño fijo para que el botón no estire
                        margin=(16, 0, 0, 0)  # Eliminar márgenes adicionales
                    ),
                ),
                pn.Row(
                    self.error_message,  # Mensaje de error
                ),
                pn.Column(
                    # Añadir el RadioButtonGroup para seleccionar la métrica
                    pn.Row(
                        self.plot_option,
                        self.download_button_pdf,
                        self.download_button_txt,
                        # Usamos un Column para aplicar un espaciado
                        align='start',
                    ),
                    pn.Row(
                        self.plot_pane,  # Gráfica
                    ),
                ),
                max_width=1000  # Ancho fijo para esta columna
            ),
            sizing_mode="stretch_width"  # Se adapta al tamaño de la pantalla
        )
        # Mostrar el layout
        pn.extension()
        layout.show()



    def actualizar_plot(self):
        self.plot.renderers = []  # Clear previous renderers
        self.plot.yaxis.axis_label = self.plot_option.value  # Update y-axis label

        if self.presenter.radius_value is None:
            return

        colors = Category10[10]  # Use a color palette with 10 colors
        color_index = 0
        legend_items = []

        # Eliminar las leyendas existentes
        self.plot.legend.items = []

        for material_name, data in self.presenter.get_material_data().items():
            #que lo llame el presenter
            results = calculo.calculate_mie_arrays(data, float(self.presenter.radius_value), float(self.presenter.n_surrounding_value))
            x = data['lambda']
            y = results[self.plot_option.value]
            color = colors[color_index % len(colors)]  # Cycle through colors
            line = self.plot.line(x, y, line_width=2, color=color)
            legend_items.append(LegendItem(label=f'{self.plot_option.value} {material_name}', renderers=[line]))
            color_index += 1

        # Crear la leyenda y añadirla a la gráfica
        legend = Legend(items=legend_items, location="top_right")  # Ajusta la ubicación de la leyenda
        self.plot.add_layout(legend, 'center')  # 'center' coloca la leyenda sobre la gráfica


    # Función para manejar la entrada del radio
    def store_radius(self,event):
        try:
            r = float(self.radius_input.value)
            if r <= 0:
                raise ValueError("Radius value must be greater than 0")
            self.presenter.update_radius(r)
            self.actualizar_plot()
            self.error_message.object = ""
        except ValueError:
            self.error_message.object = "Error: Introduce a valid value for radius"



    # Función para manejar la entrada del n del medio
    def store_n_surrounding(self, event):
        try:
            n = float(self.n_surrounding_input.value) if self.n_surrounding_input.value else 1.0
            if n <= 0:
                raise ValueError("The value of the refractive index of the medium must be greater than 0")
            self.presenter.update_n_surrounding(n)
            self.actualizar_plot()
            self.error_message.object = ""
        except ValueError:
            self.error_message.object = "Error: Enter a valid value for the refractive index of the medium"




