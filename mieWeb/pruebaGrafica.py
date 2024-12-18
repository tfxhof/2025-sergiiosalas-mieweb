from bokeh.plotting import figure, show
from bokeh.models import HoverTool

# Datos de ejemplo
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

# Crear una figura
p = figure(title="Gráfica interactiva con Zoom y Hover", x_axis_label='Eje X', y_axis_label='Eje Y', tools="pan,box_zoom,reset")

# Añadir los puntos y la línea
p.line(x, y, legend_label="Linea", line_width=2)

# Añadir el HoverTool (muestra información sobre los puntos)
hover = HoverTool()
hover.tooltips = [("X", "$x"), ("Y", "$y")]
p.add_tools(hover)

# Mostrar la gráfica
show(p)
