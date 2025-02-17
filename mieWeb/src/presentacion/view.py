import io
import sqlite3
import panel as pn
import self
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
from src.negocio.presenter import nombres_materiales, Presenter
from src.presentacion.IView import IView
from src.negocio import calculo, descarga

class View(IView):
    def __init__(self, presenter):
        self.presenter = presenter  # Se guarda la instancia de Presenter

    def show(self):
        # Mostrar el layout
        pn.extension()
        layout.show()




presenter = Presenter(100)  # Se crea una instancia de Presenter

# Crear un widget de selección múltiple con Panel
multi_choice = pn.widgets.MultiChoice(
    name="Select materials",
    options=nombres_materiales,
    width=350,
    placeholder="Select the materials you wish to compare"
)

# Contenedor para los widgets de selección de páginas
page_selectors = pn.Column(sizing_mode="stretch_width")

# Mensaje de error
error_message = pn.pane.Markdown("", sizing_mode="stretch_width")

# Initialize Bokeh output
output_notebook()

# Create a Bokeh figure with fixed dimensions
plot = figure(
    x_axis_label='Wavelength (nm)',
    y_axis_label='qext',
    tools="pan,box_zoom,reset,hover",
    tooltips=[("Wavelength", "@x"), ("Value", "@y")],
    width=500,  # Fixed width
    height=500  # Fixed height
)

# Crear el contenedor para la gráfica sin leyenda
plot_pane = pn.pane.Bokeh(plot, sizing_mode="stretch_both", min_height=400, min_width=400, max_height=50, max_width=500)

# Añadimos un RadioButtonGroup para seleccionar qué graficar
plot_option = pn.widgets.RadioBoxGroup(
    name='Select metric to plot',
    options=['qext', 'qsca', 'qabs'],
    value='qext',  # Valor predeterminado
    inline=True
)

# Conectar el RadioButtonGroup para actualizar la gráfica cuando se cambie la opción
plot_option.param.watch(lambda event: actualizar_plot(), 'value')

def actualizar_plot():
    plot.renderers = []  # Clear previous renderers
    plot.yaxis.axis_label = plot_option.value  # Update y-axis label

    if Presenter.radius_value is None:
        return

    colors = Category10[10]  # Use a color palette with 10 colors
    color_index = 0
    legend_items = []

    # Eliminar las leyendas existentes
    plot.legend.items = []

    for material_name, data in Presenter.material_data.items():
        results = calculo.calculate_mie_arrays(data, float(Presenter.radius_value), float(Presenter.n_surrounding_value))
        x = data['lambda']
        y = results[plot_option.value]
        color = colors[color_index % len(colors)]  # Cycle through colors
        line = plot.line(x, y, line_width=2, color=color)
        legend_items.append(LegendItem(label=f'{plot_option.value} {material_name}', renderers=[line]))
        color_index += 1

    # Crear la leyenda y añadirla a la gráfica
    legend = Legend(items=legend_items, location="top_right")  # Ajusta la ubicación de la leyenda
    plot.add_layout(legend, 'center')  # 'center' coloca la leyenda sobre la gráfica


# Función para manejar la entrada del radio
def store_radius(event):
    try:
        Presenter.radius_value = float(radius_input.value)
        if Presenter.radius_value <= 0:
            raise ValueError("Radius value must be greater than 0")
        actualizar_plot()
        error_message.object = ""
    except ValueError:
        error_message.object = "Error: Introduce a valid value for radius"

# Crear una entrada de texto para el radio
radius_input = pn.widgets.TextInput(
    name='Radius (nm)',
    placeholder='Enter the radius value in nanometers',
    width=300
)

# Botón para confirmar el radio
confirm_radius_button = pn.widgets.Button(
    name='Confirm radius',
    button_type='primary',
    width=50
)



# Adjuntar la función store_radius al evento del botón
confirm_radius_button.on_click(store_radius)

# Función para manejar la entrada del n del medio
def store_n_surrounding(event):
    try:
        Presenter.n_surrounding_value = float(n_surrounding_input.value) if n_surrounding_input.value else 1.0
        if Presenter.n_surrounding_value <= 0:
            raise ValueError("The value of the refractive index of the medium must be greater than 0")
        actualizar_plot()
        error_message.object = ""
    except ValueError:
        error_message.object = "Error: Enter a valid value for the refractive index of the medium"

# Crear una entrada de texto para el n del medio
n_surrounding_input = pn.widgets.TextInput(
    name='Refractive index of the medium',
    placeholder='Enter value',
    value='1',  # Valor predeterminado
    width=300
)

# Botón para confirmar el n del medio
confirm_n_surrounding_button = pn.widgets.Button(
    name='Confirm value',
    button_type='primary',
    width=50
)

# Crear un botón para descargar la gráfica como PDF
download_button_pdf = pn.widgets.Button(
    name="Download as PDF",
    button_type="primary",
    width=200
)



download_button_txt = pn.widgets.FileDownload(
    button_type='primary',
    callback=lambda: descarga.descargar_txt(Presenter.radius_value, Presenter.n_surrounding_value),
    filename="materials.zip"
)

# Adjuntar la función store_n_surrounding al evento del botón
confirm_n_surrounding_button.on_click(store_n_surrounding)



# Conectar la función mostrar_seleccion al multi-choice
multi_choice.param.watch(lambda event: IPresenter.mostrar_seleccion(event, page_selectors, plot, plot_option), 'value')



# Actualizar el layout para incluir el RadioButtonGroup encima de la gráfica
layout = pn.Row(
    # Columna izquierda: Selector de materiales y páginas
    pn.Column(
        multi_choice,  # Selector de materiales
        page_selectors,  # Selectores de páginas dinámicos
        width=400  # Ancho fijo para esta columna
    ),
    # Columna central: Radio, gráfica y botón de descarga
    pn.Column(
        pn.Row(
            radius_input,  # Entrada para el radio
            pn.Column(  # Usamos un Column para aplicar un espaciado
                confirm_radius_button,  # Botón para confirmar el radio
                sizing_mode='fixed',  # Tamaño fijo para que el botón no estire
                margin=(16, 0, 0, 0)  # Eliminar márgenes adicionales
            ),
        ),
        pn.Row(
            n_surrounding_input,  # Entrada para el n del medio
            pn.Column(  # Usamos un Column para aplicar un espaciado
                confirm_n_surrounding_button,  # Botón para confirmar el n del medio
                sizing_mode='fixed',  # Tamaño fijo para que el botón no estire
                margin=(16, 0, 0, 0)  # Eliminar márgenes adicionales
            ),
        ),
        pn.Row(
            error_message,  # Mensaje de error
        ),
        pn.Column(
              # Añadir el RadioButtonGroup para seleccionar la métrica
            pn.Row(
                plot_option,
                download_button_pdf,
                download_button_txt,
                # Usamos un Column para aplicar un espaciado
                align='start',
            ),
            pn.Row(
                plot_pane,  # Gráfica
            ),
        ),
        max_width=1000  # Ancho fijo para esta columna
    ),
    sizing_mode="stretch_width"  # Se adapta al tamaño de la pantalla
)



# Inicializar la gráfica
actualizar_plot()

