
#%%
from multiprocessing.sharedctypes import Value
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys


df_latent = pd.read_csv('output/table_8.csv', index_col=0)
df_4 = pd.read_csv('output/table_4.csv', index_col=0)
df_5 = pd.read_csv('output/table_5.csv', index_col=0)
df_6 = pd.read_csv('output/table_6.csv', index_col=0)
df_7 = pd.read_csv('output/table_7.csv', index_col=0)


# %%
col_sel = ['Cp', 'kth', 'cost', 'class']

df_sens = pd.concat([df[col_sel] for df in [df_4, df_5, df_6, df_7]])

df_sens['Cp'] = df_sens['Cp'].astype(float)
df_sens['Cp'] = df_sens['Cp']/3600

df_sens['kth'] = df_sens['kth'].astype(float)

df_sens['cost'] = df_sens['cost'].replace('e','nan')
# df_sens['cost'] = df_sens['cost'].str.replace(',','.')
df_sens['cost'] = df_sens['cost'].astype(float)

df_sens

#%%
from bokeh.models import ColumnDataSource, HoverTool, Range1d
from bokeh.plotting import figure, output_notebook, show
from bokeh.transform import factor_cmap
output_notebook()

source_lat = ColumnDataSource(df_latent)
p_lat = figure(x_axis_type='log')
p_lat.yaxis.axis_label = 'Specific Latent Heat (kWh/kg)'
p_lat.xaxis.axis_label = 'Material Cost ($/kg)'
p_lat.x_range = Range1d(1,1e4)
p_lat.y_range = Range1d(1e-3,.400)

hovertool = HoverTool(tooltips=[
    ('name', '@material'),
    ('class', '@class'),
    ])
p_lat.add_tools(hovertool)

colors = factor_cmap('class', 'Category20_15', df_latent['class'].unique())
p_lat.circle(source=source_lat, x='cost',y='sp_latent_heat', color=colors, legend_group='class', size=10)



source_sens = ColumnDataSource(df_sens.reset_index())
p_sens = figure(x_axis_type='log')
p_sens.yaxis.axis_label = 'Specific Heat (kWh/kg/K)'
p_sens.xaxis.axis_label = 'Material Cost ($/kg)'
p_sens.x_range = Range1d(8e-2,1e3)
p_sens.y_range = Range1d(0,1e-3)

hovertool = HoverTool(tooltips=[
    ('name', '@name'),
    ('class', '@class'),
    ])
p_sens.add_tools(hovertool)

colors = factor_cmap('class', 'Category10_5', df_sens['class'].unique())
p_sens.circle(source=source_sens, x='cost',y='Cp', color=colors, legend_group='class', size=10)


## Interactive Elements

from bokeh.models import CustomJS, Slider
deltaT_slider = Slider(start=100, end=1000, value=300, step=100, title="Sensible Delta T (K)")
energy_cost_slider = Slider(start=1, end=100, value=10, step=1, title="Energy Capital Cost ($/kWh)")

mat_cost = np.logspace(-1,4, 50)

source_fom= ColumnDataSource(data=dict(
    mat_cost = mat_cost,
    min_latent_heat = mat_cost/energy_cost_slider.value,
    min_specific_heat = mat_cost/(energy_cost_slider.value*deltaT_slider.value)
))

callback_fom = CustomJS(args = dict(
    source=source_fom,
    deltaT_slider = deltaT_slider,
    energy_cost_slider = energy_cost_slider
),
code = """
const data = source.data;
const deltaT = deltaT_slider.value;
const energy_cost = energy_cost_slider.value;

const mat_cost = data['mat_cost']
const min_latent_heat = data['min_latent_heat']
const min_specific_heat = data['min_specific_heat']

for (let i = 0; i < mat_cost.length; i++) {
    min_latent_heat[i] = mat_cost[i]/energy_cost;
    min_specific_heat[i] = mat_cost[i]/(energy_cost*deltaT);
}

source.change.emit();
"""
)
deltaT_slider.js_on_change('value', callback_fom)
energy_cost_slider.js_on_change('value', callback_fom)

p_sens.line('mat_cost', 'min_specific_heat', source=source_fom)
p_lat.line('mat_cost', 'min_latent_heat', source=source_fom)


## Layout

from bokeh.layouts import layout, row, column
from bokeh.models import Div


l = layout([
    column([
    Div(text="""
    <h1> Thermal Energy Storage Materials Economics </h1>
    Data taken from Alva et al 2018 (An overview of thermal energy storage systems). The only difference is that the cost of the rock thermal storage material has been set to 0.1$/kg
    <p>
    The data points represent data from the tables. The blue lines represent the minimum specific/latent heat required to achieve a overall energy capital cost specified in the slider (datapoints to the right are uneconomical). For the sensible material plot the deltaT must also be specified by the slider. Mouse over the points for more information.
    </p>
    <p>
    <h3>Equations:</h3> 
    min_latent_heat = material_cost/energy_capital_cost
    <br> min_specific_heat = material_cost/(energy_capital_cost*deltaT)
    </p>
    
    """),
    row([energy_cost_slider, deltaT_slider]),
    row([
        column([
            Div(text="""<h1>Latent TES Materials (Table 8)"""),
            p_lat
            ]),
        column([
            Div(text="""<h1>Sensible TES Materials (Tables 4-7)"""),
            p_sens
            ]),
    ])
])
])

show(l)

# %%





#%%
from bokeh.io import output_file

output_file('alva_bokeh.html')
show(l)
# %%

# %%
