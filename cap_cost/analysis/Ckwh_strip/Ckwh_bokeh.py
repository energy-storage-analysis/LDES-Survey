#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 12})

import iqplot
from bokeh.io import show, output_file, save

import os
from os.path import join as pjoin
output_dir = 'output'
if not os.path.exists(output_dir): os.makedirs(output_dir)

from es_utils.units import read_pint_df

from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

palette = pd.read_csv('../energy_colors.csv', index_col=0)['color'].to_dict()
palette = {key.replace('\\n','\n'): val for key,val in palette.items()}

df_all = read_pint_df(pjoin(REPO_DIR, 'cap_cost/data_consolidated/SM_data.csv'), index_col=[0,1], drop_units=True).reset_index('SM_type')

df_all = df_all.dropna(subset=['C_kwh'])

display_text = pd.read_csv('../tech_lookup.csv', index_col=0)

df_all['SM_type'] = df_all['SM_type'].str.replace("(","\n(", regex=False)

df_all['display_text'] = [display_text['long_name'][s].replace('\\n','\n') for s in df_all['SM_type'].values]
df_all['energy_type'] = [display_text['energy_type'][s].replace('\\n','\n') for s in df_all['SM_type'].values]
df_all['coupled'] = [display_text['coupled'][s].replace('\\n','\n') for s in df_all['SM_type'].values]
df_all['C_kwh_log'] = np.log10(df_all['C_kwh'])

median_Ckwh = df_all.groupby('SM_type')['C_kwh'].median().to_dict()

df_all['Ckwh_SMtype_median'] = df_all['SM_type'].map(median_Ckwh)
df_all = df_all.sort_values('Ckwh_SMtype_median')#.sort_values('energy_type')

# %%
#Raw entries

df_vis = df_all.reset_index().dropna(subset= ['C_kwh'])
tips = [('index','@SM_name'),  ('SM_sources','@SM_sources'), ('price_sources', '@price_sources'), ('specific price ($/kg)', '@specific_price'), ('specific energy (kWh/kg)','@specific_energy') ]

figure = iqplot.strip(
    data=df_vis, cats='SM_type', q='C_kwh', color_column='energy_type',
    q_axis='y',y_axis_type='log' ,
    show_legend=True,
    jitter=True,
    tooltips= tips,
    plot_width = 1200,plot_height=700,
    marker_kwargs={'size':10}
    )

figure.legend.location = 'bottom_right'
figure.legend.title = 'Energy Type'

figure.xaxis.major_label_orientation = np.pi/4
figure.yaxis.axis_label = "Material Energy Capital Cost ($/kWh)"
# show(figure)
figure.yaxis.axis_label_text_font_size = "16pt"
figure.xaxis.major_label_text_font_size = "16pt"

output_file(pjoin(output_dir,'Ckwh_bokeh.html'))
save(figure)