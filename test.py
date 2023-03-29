from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider, CustomJS
from bokeh.plotting import figure, output_file, show
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import sensitivity as sns

x = np.linspace(0, 10, 500)
y = np.sin(x)

source = ColumnDataSource(data=dict(x=x, y=y))

# Create plots and widgets
plot = figure()

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.5)

# Create Slider object
slider = Slider(start=0, end=6, value=2,
				step=0.2, title='Number of points')

# Adding callback code
callback = CustomJS(args=dict(source=source, val=slider),
					code="""
	const data = source.data;
	const freq = val.value;
	const x = data['x'];
	const y = data['y'];
for (var i = 0; i < x.length; i++) {
		y[i] = Math.sin(freq*x[i]);
	}
	
	source.change.emit();
""")

slider.js_on_change('value', callback)

# Arrange plots and widgets in layouts
layout = column(slider, plot)

output_file('exam.html')

show(layout)
