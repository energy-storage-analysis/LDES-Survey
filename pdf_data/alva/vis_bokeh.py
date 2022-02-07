
#%%
from multiprocessing.sharedctypes import Value
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append('..')

df_latent = pd.read_csv('output/table_8.csv')

df_latent.columns = df_latent.columns.str.replace(r'\r\n',r'\n', regex=True)

df_latent = df_latent.rename(
    {'Type  ': 'type',
       'Class  ': 'class', 
       'Thermal storage material  ': 'material',
       'Phase change temperature (degC) ': 'phase_change_T',
       'Latent heat (kJ$kg\n-1) ': 'sp_latent_heat',
       '-3)\nDensity (kg$m  ': 'density',
       'Thermal conductivity (W$m\n-1 K\n-1)': 'kth',
       'Latent heat storage capacity (MJ$m\n-3) ': 'vol_latent_heat',
       'Technical grade cost ($$kg\n-1) ': 'cost',
       'Remarks  ':'remarks'},
axis=1)

df_latent = df_latent.drop('type',axis=1)
df_latent = df_latent.drop('Unnamed: 0',axis=1)
df_latent = df_latent.drop('remarks',axis=1)

df_latent['phase_change_T'] = df_latent['phase_change_T'].replace('40-45', '42.5')
df_latent['phase_change_T'] = df_latent['phase_change_T'].astype(float)

df_latent['sp_latent_heat'] = df_latent['sp_latent_heat'].astype(float)
df_latent['sp_latent_heat'] = df_latent['sp_latent_heat']/3600

df_latent['class'] = df_latent['class'].fillna(method='ffill') 
df_latent['class'] = df_latent['class'].replace('eutectics', 'Organic', regex=True)
df_latent['class'] = df_latent['class'].replace('Organic', 'Organic Eutectic', regex=True)
df_latent['class'] = df_latent['class'].replace('Inorganic ', '', regex=True)
df_latent['cost'] = df_latent['cost'].dropna().replace('\(RG\)','', regex=True).astype(float)

df_latent.info()
# %%

df_4 = pd.read_csv('output/table_4.csv')
df_4.columns = [c.strip() for c in df_4.columns]
df_4 = df_4.dropna(subset=['Property'])
df_4 = df_4.T
df_4.columns = df_4.iloc[1]
df_4 = df_4.iloc[2:]
df_4.columns = df_4.columns.str.replace(r'\r\n',r'\n', regex=True)

df_4['class'] = 'Thermal Oils'
df_4 = df_4.rename({  
    '-1 degC\n-1)\nSpeciﬁc heat capacity at 210 degC (kJ kg': 'Cp',
    'Thermal conductivity at 210 degC (W m\n-1 K\n-1)': 'kth',
    'Cost (V$t\n-1)': 'cost'
    }, axis=1)
df_4.index.name = 'name'

df_4['cost'] = df_4['cost'].str.replace(',','.')

df_4

# %%
df_5 = pd.read_csv('output/table_5.csv')
df_5.columns = [c.strip() for c in df_5.columns]
df_5 = df_5.drop('Unnamed: 0', axis=1)
df_5.columns = df_5.columns.str.replace(r'\r\n',r'\n', regex=True)

df_5 = df_5.dropna(subset=['Highest operating temperature (degC)'])
df_5['class'] = 'Molten Salt'

df_5 = df_5.rename({
    'Salt/eutectic': 'name',
    'Speciﬁc heat (kJ$kg\n-1 degC\n-1)': 'Cp',
    'Thermal conductivity (W$m\n-1 K\n-1)': 'kth',
    'Cost ($$kg\n-1)': 'cost'
    }, axis=1)


df_5 = df_5.set_index('name')

df_5 = df_5.drop('LiNO3')

df_5

# %%

df_6 = pd.read_csv('output/table_6.csv')
df_6.columns = [c.strip() for c in df_6.columns]
df_6 = df_6.drop('Unnamed: 0', axis=1)
df_6.columns = df_6.columns.str.replace(r'\r\n',r'\n', regex=True)

df_6['class'] = 'Metal Alloy'
df_6 = df_6.rename({
    'Metal/Alloy': 'name',
    'Speciﬁc heat -1\nkJ$kg\n-1 degC': 'Cp',
    'Thermal conductivity (W$m\n-1 K\n-1)' : 'kth',
    'Cost ($$kg\n-1)': 'cost'
    }, axis=1)

df_6 = df_6.set_index('name')
df_6

# %%

df_7 = pd.read_csv('output/table_7.csv')
df_7.columns = [c.strip() for c in df_7.columns]
df_7 = df_7.drop('Unnamed: 0', axis=1)
df_7 = df_7.dropna(subset=['Type'])
df_7['class'] = 'Rocks'
df_7['cost'] = 0.1
df_7.columns = df_7.columns.str.replace(r'\r\n',r'\n', regex=True)

df_7 = df_7.rename({
    'Rock': 'name',
    'Speciﬁc heat (kJ$kg\n-1 degC\n-1) @20 degC': 'Cp',
    'Thermal conductivity (W$m\n-1 K\n-1)': 'kth',
    }, axis=1)

df_7 = df_7.set_index('name')

import re
def average_range(s):
    m = re.search("(\S+)-(\S+)", s)
    
    if m is None:
        return s
    else:
        f1 = float(m.groups()[0])
        f2 = float(m.groups()[1])

        return (f1 + f2)/2

df_7['Cp'] = df_7['Cp'].apply(average_range)
df_7

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
