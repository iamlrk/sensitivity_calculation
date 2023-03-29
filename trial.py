# Bokeh libraries
from bokeh.io import output_file, output_notebook
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from bokeh.layouts import row, column, gridplot
from bokeh.models.widgets import Tabs, Panel
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import sensitivity as sns

output_file('filename.html')

bg_curves = pd.read_csv('bgcurves.csv')
energies = bg_curves['energy'].values # keV
mass_attentuation_coefficients = bg_curves['massatt'].values
background_values = {
    'density' : 5.85, # g/cc
    'shield_thickness' : 10, # cm 
    'mass_attentuation_coefficients' : mass_attentuation_coefficients, 
    'energies' : energies, # keV
    'solid_angle' : 1.4, # sterdaiens
    'shield_leakage_bg_count_rates' : bg_curves['fig8'].values,
    'rigidity_cut_off' : 1.3,  
    'energy_counts' : bg_curves['fig5'].values,
    'thickness': 0.2, # cm
    'area': 5200, # cm^2
}
bg_noise = sns.Background(**background_values)
background = bg_noise.calculate_bg()
fig, ax = plt.subplots()
a = bg_noise.ploty(ax)