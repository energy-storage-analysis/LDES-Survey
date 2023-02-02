#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
from es_utils.units import read_pint_df
plt.rcParams.update({'font.size':16, 'savefig.dpi': 600})

import os
from os.path import join as pjoin
output_dir = 'output'
if not os.path.exists(output_dir): os.makedirs(output_dir)

from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

df = read_pint_df(pjoin(REPO_DIR, 'cap_cost/data_consolidated/SM_data.csv'), index_col=[0,1], drop_units=True).reset_index('SM_type')
#%%


# df = df.where(df['SM_type'].isin([
#     'flow_battery',
#     'hybrid_flow'
# ])).dropna(subset=['SM_type'])



# Bokeh plot with all tech 
from bokeh.plotting import figure, show, save, output_file
from bokeh.models import HoverTool

energy_densities_line = np.logspace(
    np.log10(df['specific_energy'].min()),
    np.log10(df['specific_energy'].max()),
    )

#Mat cost for given C_kwh
mat_cost_line = energy_densities_line*10
SM_types = df['SM_type'].unique()

#https://docs.bokeh.org/en/latest/docs/user_guide/plotting.html#userguide-plotting-scatter-markers
MARKERS = ['circle','square','triangle','star','plus','inverted_triangle','hex','diamond','square_pin','square_x']*2

if len(SM_types) <= 10:
    color_category = 'Category10_{}'.format(len(SM_types))
else:
    color_category = 'Category20_{}'.format(len(SM_types))

#TODO: Temporary override not using factor_cmap for separated scatter plot. How to specify cmap by string. 
from bokeh.palettes import Category20_15, Category20_17
color_category = Category20_17

#%%
p = figure(background_fill_color="#fafafa", y_axis_type='log',x_axis_type='log',plot_width=1200,plot_height=700)

p.xaxis.axis_label = 'Energy Density (kWh/kg)'
p.yaxis.axis_label = 'Material Cost ($/kg)'



for i, SM_type in enumerate(SM_types):
    df_sel = df.where(df['SM_type'] == SM_type).dropna(subset=['SM_type'])

    points = p.scatter("specific_energy", "specific_price", source=df_sel,
            fill_alpha=1, size=15,
            legend_label=SM_type,
            marker= MARKERS[i],
            color=color_category[i]
    )

    points.muted = False

p.line(energy_densities_line, mat_cost_line)


p.legend.location = "top_left"
p.legend.title = "Storage Medium Type"

hovertool = HoverTool(tooltips=[
    ('SM name','@SM_name'), 
    ('Specific Energy (kWh/kg)','@specific_energy'), 
    ('Specific Price ($/kg)','@specific_price'), 
    ('$/kWh','@C_kwh'), 
    ('SM_sources','@SM_sources'), 
    ('price_sources', '@price_sources'),
    ('materials', '@materials'),
    ('notes', '@notes')
    ])

p.add_tools(hovertool)
p.legend.click_policy="mute"

p.yaxis.axis_label_text_font_size = "16pt"
p.xaxis.major_label_text_font_size = "16pt"

output_file(pjoin(output_dir,'Ckwh_line_bokeh.html'))
save(p)



#%%



