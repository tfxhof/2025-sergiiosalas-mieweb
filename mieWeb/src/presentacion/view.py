import panel as pn
from bokeh.io import output_notebook
from bokeh.models import Legend, LegendItem
from bokeh.palettes import Category10
from bokeh.plotting import figure
from src.negocio.IPresenter import IPresenter
from src.presentacion.IView import IView
from src.negocio.descarga import descargar_txt

class View(IView):
    def __init__(self, presenter: IPresenter):
        pn.extension() # Inicializar Panel

        self.presenter = presenter  # Se guarda la instancia de Presenter

        # Mensaje de error
        self.error_message = pn.pane.Markdown("", sizing_mode="stretch_width")

        # Crear un widget de selección múltiple con Panel
        self.multi_choice = pn.widgets.MultiChoice(
            name="Select materials",
            options= self.presenter.get_nombres_materiales(),
            width=320,
            placeholder="Select the materials to compare"
        )

        # Contenedor para los widgets de selección de páginas
        self.page_selectors = pn.Column(sizing_mode="stretch_width")

        # Create a Bokeh figure with fixed dimensions
        self.plot = figure(
            x_axis_label='Wavelength (nm)',
            y_axis_label='qext',
            tools="pan,box_zoom,reset,hover, save",
            tooltips=[("Wavelength", "@x"), ("Value", "@y")],
            width=500,  # Fixed width
            height=500,  # Fixed height
            output_backend = "svg"  # Enable SVG output
        )

        # Crear el contenedor para la gráfica sin leyenda
        self.plot_pane = pn.pane.Bokeh(self.plot,
                                       sizing_mode="stretch_both",
                                       min_height=400,
                                       max_height=500,
                                       min_width=400,
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
            lambda event: self.manejar_seleccion(event), 'value')

        # Crear una entrada de texto para el radio
        self.radius_input = pn.widgets.TextInput(
            name='Radius (nm)',
            placeholder='Enter the radius value in nanometers',
            value='50',  # Valor predeterminado
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
            width=300,
        )

        # Botón para confirmar el n del medio
        self.confirm_n_surrounding_button = pn.widgets.Button(
            name='Confirm value',
            button_type='primary',
            width=50
        )

        # Adjuntar la función store_n_surrounding al evento del botón
        self.confirm_n_surrounding_button.on_click(self.store_n_surrounding)

        # Botón para descargar los resultados
        self.download_button_txt = pn.widgets.FileDownload(
            label="Download efficiencies (q)",
            button_type='primary',
            callback=lambda: descargar_txt(self.presenter),
            filename="efficiencies.zip"
        )

        # Crear un botón de información
        self.info_button = pn.widgets.Button(
            name="Instructions",
            button_type="warning",
            width=50
        )

        # Conectar el botón para mostrar/ocultar el diálogo
        self.info_button.on_click(lambda event: self.template.open_modal())

        # Inicializar la gráfica
        self.actualizar_plot()

        sidebar = [self.radius_input, self.confirm_radius_button,
                   self.n_surrounding_input, self.confirm_n_surrounding_button,
                   self.error_message,
                   self.multi_choice, self.page_selectors]

        main = [self.plot_option,
                self.plot_pane,
                self.download_button_txt]

        self.template =  pn.template.BootstrapTemplate(
            title="Mie Web",
            header=self.info_button,
            main=main,
            sidebar=sidebar
        )

        self.template.modal.append(
            """
            # How to use the app:
            1. Select the materials you want to compare from the list.
            2. Adjust the radius and the surrounding refractive index as needed.
            3. Choose the metric (qext, qsca, or qabs) to visualize on the graph.
            4. Download the computed results in TXT or SVG format.
            """
        )

    def toggle_info_dialog(self):
        # Alternar la visibilidad del diálogo
        self.info_dialog.visible = not self.info_dialog.visible

    def show(self):
        return self.template.servable()

    # Función para actualizar la gráfica
    def actualizar_plot(self):
        self.plot.renderers = []  # Clear previous renderers
        self.plot.yaxis.axis_label = self.plot_option.value  # Update y-axis label

        data_plot = self.presenter.calcular_datos_grafica(self.plot_option.value)
        if data_plot is None:
            return

        colors = Category10[10]  # Definir colores en la vista
        legend_items = []
        color_index = 0

        # Eliminar las leyendas existentes
        self.plot.legend.items = []

        # Dibujar cada línea en la gráfica
        for material_name, x, y in data_plot:
            color = colors[color_index % len(colors)]
            line = self.plot.line(x, y, line_width=2, color=color)

            legend_item = LegendItem(label=f"{self.plot_option.value} {material_name}", renderers=[line])
            legend_items.append(legend_item)

            color_index += 1


        # Crear la leyenda y añadirla a la gráfica
        legend = Legend(items=legend_items, location="top_right")  # Ajusta la ubicación de la leyenda
        self.plot.add_layout(legend, 'center')  # 'center' coloca la leyenda sobre la gráfica

    def show_error(self, message):
        # Mensaje de error
        self.error_message.object = message


    # Función para manejar la entrada del radio
    def store_radius(self,event):
        self.presenter.radius_store(self.radius_input.value)



    # Función para manejar la entrada del n del medio
    def store_n_surrounding(self, event):
        self.presenter.n_surrounding_store(self.n_surrounding_input.value)



    def manejar_seleccion(self, event):
        seleccionados = set(event.new)
        for widget in list(self.page_selectors):
            nombre_material = widget.name.split(" for ")[1]
            if nombre_material not in seleccionados:  # Si el material fue deseleccionado
                self.page_selectors.remove(widget)  # Eliminar el selector de página
                self.presenter.remove_from_material_data(nombre_material)  # Eliminar el material de `material_data`


        for nombre in seleccionados:
            # Verifica que no exista un selector para el material
            if not any(widget.name.split(" for ")[1] == nombre for widget in self.page_selectors):

                opciones_paginas = self.presenter.obtener_opciones_paginas(nombre)

                page_selector = pn.widgets.Select(
                    name=f"Select page for {nombre}",
                    options=opciones_paginas,
                    value='Select page',
                    width=250
                )
                self.page_selectors.append(page_selector)

                #cuando el usuario cambia la página seleccionada en el selector
                def actualizar_valores(event, nombre=nombre):
                    if event.new == 'Select page':
                        self.presenter.remove_from_material_data(nombre)
                    else:
                        page_name = event.new
                        self.presenter.obtener_valores(nombre, page_name)
                    self.actualizar_plot()

                page_selector.param.watch(actualizar_valores, 'value')
        self.actualizar_plot()


    def clear_plot(self):
        pass