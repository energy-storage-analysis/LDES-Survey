#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import seaborn as sns
sys.path.append('..')

# Alva Thermal
df_latent = pd.read_csv('alva/output/table_8.csv', index_col=0)

df_latent['C_kwh'] = df_latent['cost']/(df_latent['sp_latent_heat'])
df_latent['energy_type'] = 'Latent Thermal'# (T > 200 C)'
df_latent['source'] = 'Alva et al. 2018'
df_latent = df_latent.where(df_latent['phase_change_T'] > 200).dropna(subset=['phase_change_T'])

df_latent = df_latent.rename({'material':'name'}, axis=1)

df_4 = pd.read_csv('alva/output/table_4.csv', index_col=0)
df_5 = pd.read_csv('alva/output/table_5.csv', index_col=0)
df_6 = pd.read_csv('alva/output/table_6.csv', index_col=0)
df_7 = pd.read_csv('alva/output/table_7.csv', index_col=0)

col_sel = ['Cp', 'kth', 'cost', 'class']

df_sens = pd.concat([df[col_sel] for df in [df_4, df_5, df_6, df_7]])
df_sens = df_sens.reset_index() #name was the index
df_sens['Cp'] = df_sens['Cp']/3600
df_sens['C_kwh'] = df_sens['cost']/(df_sens['Cp']*500)

df_sens['energy_type'] = 'Sensible Thermal'
df_sens['source'] = 'Alva et al. 2018'


#%%
df_ec = pd.read_csv('li_2017/output/table_2.csv', index_col=0)
df_ec = df_ec.rename({'label':'name'},axis=1)

df_ec['energy_type'] = 'Chemical (electrochemical)'
df_ec['source'] = 'Li et al. 2017'

#%%

# df_virial = pd.read_csv('nomura_2017/table_2_mat.csv', index_col=0)

# df_virial['specific_energy'] = (1*df_virial['max stress'])/df_virial['density']
# df_virial['specific_energy'] = df_virial['specific_energy']/3600000
# df_virial['C_kwh'] = df_virial['mat_cost']/df_virial['specific_energy']


#%%

from kale_2018.vis import load_tables

kale_tables = load_tables('kale_2018')

kale_tables['a1']['energy_type'] = 'Virial (Metal)'
kale_tables['a1']['source'] = 'Kale 2018'
kale_tables['a1'] = kale_tables['a1'].rename({'Material': 'name'}, axis=1)

kale_tables['a2']['energy_type'] = 'Virial (Composite)'
kale_tables['a2']['source'] = 'Kale 2018'
kale_tables['a2'] = kale_tables['a2'].rename({'Material': 'name'}, axis=1)

#%%

cols = ['C_kwh','energy_type','source','name']

df_all = pd.concat([
df_latent[cols].dropna(),
df_sens[cols].dropna(),
df_ec[cols].dropna(),
kale_tables['a1'][cols].dropna(),
kale_tables['a2'][cols].dropna()
])

df_all
#%%
from matplotlib import ticker as mticker
plt.rcParams.update({'font.size': 20})

df_all['C_kwh_log'] = np.log10(df_all['C_kwh'])
df_all['cat_label'] = df_all['energy_type'] + '\n(' + df_all['source'] + ')'

fig = plt.figure(figsize = (13,6))
# plt.violinplot(dataset=df_all['C_kwh'].values)
# sns.violinplot(data=df_all, x='cat_label', y='C_kwh_log')
sns.stripplot(data=df_all, x='cat_label', y='C_kwh_log', size=10)

plt.axhline(np.log10(10), linestyle='--', color='gray')

fig.axes[0].yaxis.set_major_formatter(mticker.StrMethodFormatter("$10^{{{x:.0f}}}$"))
fig.axes[0].yaxis.set_ticks([np.log10(x) for p in range(-1,4) for x in np.linspace(10**p, 10**(p+1), 10)], minor=True)
# plt.gca().set_xticks(np.arange(0, len(labels)), labels=labels)

# plt.yscale('log')
plt.xticks(rotation=45)
plt.ylabel('Material Energy Cost ($/kWh)')
# %%
import iqplot
from bokeh.io import output_notebook, show
from bokeh.models import ColumnDataSource, HoverTool, Range1d
from bokeh.io import output_file

# output_notebook()

# source = ColumnDataSource(df_all)

figure = iqplot.strip(
    data=df_all, cats='cat_label', q='C_kwh', 
    q_axis='y',y_axis_type='log' ,
    jitter=True,
    tooltips=[('name','@name')],
    plot_width = 1000,plot_height=700,
    marker_kwargs={'size':10}
    )

figure.xaxis.major_label_orientation = np.pi/4
figure.yaxis.axis_label = "Energy Capital Cost ($/kWh)"
# show(figure)
figure.yaxis.axis_label_text_font_size = "16pt"
figure.xaxis.major_label_text_font_size = "16pt"

output_file('mat_cost_compare.html')
show(figure)