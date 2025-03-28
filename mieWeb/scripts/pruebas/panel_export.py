from bokeh.plotting import figure
from bokeh.io.export import export_svgs
import numpy as np
import pandas as pd
import panel as pn

# Enable Panel extension
pn.extension()

# Generate random data for the line plot
np.random.seed(42)
data = pd.DataFrame({
    'x': np.linspace(0, 10, 100),
    'y': np.sin(np.linspace(0, 10, 100))
})

# Create a line plot using Bokeh
line_plot = figure(
    title="Line Plot Example",
    x_axis_label="X-axis",
    y_axis_label="Y-axis",
    width=800,
    height=800,
    output_backend="svg"  # Enable SVG output
)
line_plot.line(data['x'], data['y'], line_width=2, color="blue")

# Display the line plot in a Panel layout
dashboard = pn.Column(
    "# Line Plot with Panel",
    line_plot
)

# Serve the Panel dashboard
dashboard.servable()
