#%%``
import numpy as np
import pandas as pd
from bokeh.plotting import figure, show, save, output_file
from bokeh.transform import factor_cmap, factor_mark
from bokeh.models import HoverTool

#%%
df_Ckwh = pd.read_csv('data/C_kwh.csv', index_col=0)

df_SMs = pd.read_csv('data/SM_data.csv', index_col=0)
#TODO: duplicated in calc_Ckwh
df_SMs = df_SMs.where(df_SMs['source'] != 'Alok 2021').dropna(subset=['source'])

df_SMs = df_SMs[['materials', 'notes']]

df_SMs = df_SMs.loc[df_Ckwh.index]



df = pd.concat([df_Ckwh, df_SMs], axis=1)

# df = df.where(df['energy_type'] != 'Electrostatic (Capacitor)').dropna(subset=['energy_type'])

#%%


energy_densities_line = np.logspace(
    np.log10(df['specific_energy'].min()),
    np.log10(df['specific_energy'].max()),
    )

#Mat cost for given C_kwh
mat_cost_line = energy_densities_line*10
#%%

energy_types = df['energy_type'].unique()
energy_types

#https://docs.bokeh.org/en/latest/docs/user_guide/plotting.html#userguide-plotting-scatter-markers
MARKERS = ['circle','square','triangle','star','plus','inverted_triangle','hex','diamond','cross','square_x']
MARKERS = MARKERS[0:len(energy_types)]

color_category = 'Category10_{}'.format(len(energy_types))

#%%
p = figure(background_fill_color="#fafafa", y_axis_type='log',x_axis_type='log',plot_width=1500,plot_height=800)

p.xaxis.axis_label = 'Energy Density (kWh/kg)'
p.yaxis.axis_label = 'Material Cost ($/kg)'

p.scatter("specific_energy", "specific_price", source=df,
          legend_group="energy_type", fill_alpha=0.5, size=20,
          marker=factor_mark('energy_type', MARKERS, energy_types),
          color=factor_cmap('energy_type', color_category, energy_types))

p.line(energy_densities_line, mat_cost_line)


p.legend.location = "top_left"
p.legend.title = "energy_type"

hovertool = HoverTool(tooltips=[
    ('SM name','@SM_name'), 
    ('Specific Energy (kWh/kg)','@specific_energy'), 
    ('Specific Price ($/kg)','@specific_price'), 
    ('$/kWh','@C_kwh'), 
    ('source','@SM_source'), 
    ('price_sources', '@price_sources'),
    ('materials', '@materials'),
    ('notes', '@notes')
    ])

p.add_tools(hovertool)


output_file('output/bokeh_Ckwh.html')
save(p)


# %%
