#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df_prices = pd.read_csv('data/df_prices.csv', index_col=0)


s_prices_avg = df_prices['specific_price_avg']
s_prices_avg

#%%

df_singlemat = pd.read_csv('data/df_singlemat.csv', index_col=0) 
df_singlemat = df_singlemat.dropna(subset=['specific_energy'])

df_singlemat = df_singlemat[['energy_type','specific_energy']]

#TODO: improve handling
# df_singlemat = df
# df_singlemat = df_singlemat.where(df_singlemat['index'] != 'O3U').dropna(how='all')

df_singlemat['specific_price'] = [s_prices_avg[f] if f in s_prices_avg.index else np.nan for f in df_singlemat.index]
# df_singlemat = df_singlemat.set_index('index')

df_singlemat.info()

#%%k

df_couples = pd.read_csv('data/df_couples.csv', index_col=0) 
df_couples['SP_A'] = [s_prices_avg[f] if f in s_prices_avg.index else np.nan for f in df_couples['A']]
df_couples['SP_B'] = [s_prices_avg[f] if f in s_prices_avg.index else np.nan for f in df_couples['B']]

#TODO: chech this equation
df_couples['specific_price'] = (df_couples['SP_A']*df_couples['mu_A'] + df_couples['SP_B']*df_couples['mu_B'])/(df_couples['mu_A']+df_couples['mu_B'])


# df_couples = df_couples.rename({''})

df_couples['energy_type'] = 'EC Couple'
df_couples.index.name = 'index'

df_couples.info()

# %%

col_select = ['energy_type', 'specific_energy','specific_price']

df_all = pd.concat([
    df_singlemat[col_select],
    df_couples[col_select]
]) 
df_all
# %%


df_all['C_kwh'] = df_all['specific_price']/df_all['specific_energy']

df_all

#%%

#%%
cat_label = 'energy_type'

from matplotlib import ticker as mticker
plt.rcParams.update({'font.size': 20})

df_all['C_kwh_log'] = np.log10(df_all['C_kwh'])

fig = plt.figure(figsize = (13,8))
# plt.violinplot(dataset=df_singlemat['C_kwh'].values)
# sns.violinplot(data=df_singlemat, x='cat_label', y='C_kwh_log')
sns.stripplot(data=df_all, x=cat_label, y='C_kwh_log', size=10)

plt.axhline(np.log10(10), linestyle='--', color='gray')

fig.axes[0].yaxis.set_major_formatter(mticker.StrMethodFormatter("$10^{{{x:.0f}}}$"))
fig.axes[0].yaxis.set_ticks([np.log10(x) for p in range(-1,4) for x in np.linspace(10**p, 10**(p+1), 10)], minor=True)
# plt.gca().set_xticks(np.arange(0, len(labels)), labels=labels)

# plt.yscale('log')
plt.xticks(rotation=45)
plt.ylabel('Material Energy Cost ($/kWh)')
plt.tight_layout()
plt.savefig('output/fig_C_kwh_avgprice.png')
# %%

val_counts = df_prices['num_source'].value_counts()
present_num_sources = val_counts.index

val_counts

#%%

dfs_price_refs = []

for n in present_num_sources:
    df_price_refs = df_prices
    df_sel = df_prices.where(df_prices['num_source'] == n)
    df_sel = df_sel['specific_price_refs'].dropna().rename('specific_price').to_frame()
    df_sel['price_type'] = '{} ref.'.format(n)
    dfs_price_refs.append(df_sel)

df_prices_element = df_prices['specific_price_element'].dropna().rename('specific_price').to_frame()
df_prices_element['price_type']= 'elemental'


df_prices_2 = pd.concat([
    *dfs_price_refs,
    df_prices_element
])

# df_prices_2 = df_prices_2.reset_index()

df_prices_2

#Downselect to those preset
present_materials = [m for m in df_singlemat.index if m in df_prices_2.index]

df_prices_2 = df_prices_2.loc[set(present_materials)]

df_prices_2

#%%

df_vis = pd.merge(df_prices_2, df_singlemat[['energy_type','specific_energy']], on='index')


df_vis['C_kwh'] = df_vis['specific_price']/df_vis['specific_energy']

df_vis
# %%
cat_label = 'energy_type'

from matplotlib import ticker as mticker
plt.rcParams.update({'font.size': 20})

df_vis['C_kwh_log'] = np.log10(df_vis['C_kwh'])

fig = plt.figure(figsize = (13,8))
# plt.violinplot(dataset=df_singlemat['C_kwh'].values)
# sns.violinplot(data=df_singlemat, x='cat_label', y='C_kwh_log')
sns.stripplot(data=df_vis, x=cat_label, y='C_kwh_log', hue='price_type', size=10)

plt.axhline(np.log10(10), linestyle='--', color='gray')

fig.axes[0].yaxis.set_major_formatter(mticker.StrMethodFormatter("$10^{{{x:.0f}}}$"))
fig.axes[0].yaxis.set_ticks([np.log10(x) for p in range(-1,4) for x in np.linspace(10**p, 10**(p+1), 10)], minor=True)
# plt.gca().set_xticks(np.arange(0, len(labels)), labels=labels)

# plt.yscale('log')
plt.xticks(rotation=45)
plt.ylabel('Material Energy Cost ($/kWh)')
plt.tight_layout()

plt.savefig('output/fig_C_kwh.png')

# %%

df_vis_2 = df_vis.reset_index()

df_vis_2['specific_price'] = df_vis_2['specific_price'].map('{:,.2f}'.format)
df_vis_2['specific_energy'] = df_vis_2['specific_energy'].map('{:,.2f}'.format)

# %%



import iqplot
from bokeh.io import output_notebook, show
from bokeh.models import ColumnDataSource, HoverTool, Range1d
from bokeh.io import output_file


tips = [('index','@index'), ('price_type','@price_type'), ('specific price ($/kg)', '@specific_price'), ('specific energy (kWh/kg)','@specific_energy')]

figure = iqplot.strip(
    data=df_vis_2, cats='energy_type', q='C_kwh', 
    q_axis='y',y_axis_type='log' ,
    jitter=True,
    tooltips= tips,
    plot_width = 1000,plot_height=700,
    marker_kwargs={'size':10}
    )

figure.xaxis.major_label_orientation = np.pi/4
figure.yaxis.axis_label = "Energy Capital Cost ($/kWh)"
# show(figure)
figure.yaxis.axis_label_text_font_size = "16pt"
figure.xaxis.major_label_text_font_size = "16pt"

output_file('output/mat_cost_compare.html')
show(figure)
# %%
