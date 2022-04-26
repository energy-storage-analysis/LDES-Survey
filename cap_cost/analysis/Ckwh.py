#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import ticker as mticker
plt.rcParams.update({'font.size': 20})

import iqplot
from bokeh.io import show, output_file, save

import os
from os.path import join as pjoin
output_dir = 'output/Ckwh'
if not os.path.exists(output_dir): os.makedirs(output_dir)


palette = pd.read_csv('energy_colors.csv', index_col=0)['color'].to_dict()
palette = {key.replace('\\n','\n'): val for key,val in palette.items()}
palette

# %%

#%%

df_all = pd.read_csv('../data_consolidated/C_kWh.csv', index_col=0)
df_all = df_all.dropna(subset=['C_kwh'])

display_text = pd.read_csv('tech_lookup.csv', index_col=0)

df_all['SM_type'] = df_all['SM_type'].str.replace("(","\n(", regex=False)

df_all['display_text'] = [display_text['long_name'][s].replace('\\n','\n') for s in df_all['SM_type'].values]
df_all['energy_type'] = [display_text['energy_type'][s].replace('\\n','\n') for s in df_all['SM_type'].values]
df_all['C_kwh_log'] = np.log10(df_all['C_kwh'])

#%%

median_Ckwh = df_all.groupby('SM_type')['C_kwh'].median().to_dict()

df_all['Ckwh_SMtype_median'] = df_all['SM_type'].map(median_Ckwh)

df_all = df_all.sort_values('Ckwh_SMtype_median')#.sort_values('energy_type')

#%%
cat_label = 'display_text'

df_plot = df_all
fig = plt.figure(figsize = (18,8))
sns.stripplot(data=df_plot, x=cat_label, y='C_kwh_log', size=10, hue='energy_type', palette=palette)

plt.axhline(np.log10(10), linestyle='--', color='gray')

fig.axes[0].yaxis.set_major_formatter(mticker.StrMethodFormatter("$10^{{{x:.0f}}}$"))
log_ticks = range(int(np.floor(df_plot['C_kwh_log'].min())), int(np.ceil(df_plot['C_kwh_log'].max())))

fig.axes[0].yaxis.set_ticks([np.log10(x) for p in log_ticks for x in np.linspace(10**p, 10**(p+1), 10)], minor=True)
plt.xticks(rotation=90)

plt.gca().get_legend().set_bbox_to_anchor([0,0,1.35,1])

plt.ylabel('Material Energy Cost ($/kWh)')
plt.xlabel('Technology')
plt.suptitle("{} Storage Media with Price and Energy data".format(len(df_plot)))

plt.tight_layout()
plt.savefig(pjoin(output_dir,'Ckwh.png'))

#%%

elim_types = [
    'dielectric_capacitor',
    'EDLC',
    'pseudocapacitor',
    'gravitational',
    'pressure_cavern',
    'pressure_tank',
    'smes',
    'flywheel'
    ]


df_elim = df_all[df_all['SM_type'].isin(elim_types)]


df_elim['SM_type'] = pd.Categorical(df_elim['SM_type'], categories=elim_types, ordered=True)
df_elim = df_elim.sort_values('SM_type')

df_elim = df_elim[df_elim['C_kwh']<1e4]#.dropna(how='all')

df_plot = df_elim
fig = plt.figure(figsize = (8,7))
sns.stripplot(data=df_plot, x=cat_label, y='C_kwh_log', size=10, hue='energy_type', palette=palette)

plt.axhline(np.log10(10), linestyle='--', color='gray')

# plt.ylim(1,4)
fig.axes[0].yaxis.set_major_formatter(mticker.StrMethodFormatter("$10^{{{x:.0f}}}$"))

log_ticks = range(int(np.floor(df_plot['C_kwh_log'].min())), int(np.ceil(df_plot['C_kwh_log'].max())))

fig.axes[0].yaxis.set_ticks([np.log10(x) for p in log_ticks for x in np.linspace(10**p, 10**(p+1), 10)], minor=True)
plt.xticks(rotation=90)

# plt.gca().get_legend().set_bbox_to_anchor([0,0,1.5,1])
plt.gca().get_legend().remove()

plt.ylabel('Material Energy Cost ($/kWh)')
plt.xlabel('Technology')
plt.suptitle("{} Storage Media with Price and Energy data".format(len(df_plot)))


plt.tight_layout()
plt.savefig(pjoin(output_dir,'Ckwh_eliminate.png'))

#%%

ec_types = [
    'solid_electrode',
    'liquid_metal_battery',
    'metal_air',
    'hybrid_flow',
    'flow_battery',
    'synfuel'
    ]


df_ec = df_all[df_all['SM_type'].isin(ec_types)]


df_ec['SM_type'] = pd.Categorical(df_ec['SM_type'], categories=ec_types, ordered=True)
df_ec = df_ec.sort_values('SM_type')

df_ec = df_ec[df_ec['C_kwh']<1e4]#.dropna(how='all')

df_plot = df_ec
fig = plt.figure(figsize = (8,8))
sns.stripplot(data=df_plot, x=cat_label, y='C_kwh_log', size=10, hue='energy_type', palette=palette)

plt.axhline(np.log10(10), linestyle='--', color='gray')

# plt.ylim(1,4)
fig.axes[0].yaxis.set_major_formatter(mticker.StrMethodFormatter("$10^{{{x:.0f}}}$"))
log_ticks = range(int(np.floor(df_plot['C_kwh_log'].min())), int(np.ceil(df_plot['C_kwh_log'].max())))

fig.axes[0].yaxis.set_ticks([np.log10(x) for p in log_ticks for x in np.linspace(10**p, 10**(p+1), 10)], minor=True)
plt.xticks(rotation=90)

# plt.gca().get_legend().set_bbox_to_anchor([0,0,1.5,1])
plt.gca().get_legend().remove()

plt.ylabel('Material Energy Cost ($/kWh)')
plt.xlabel('Technology')
plt.suptitle("{} Storage Media with Price and Energy data".format(len(df_plot)))


plt.tight_layout()
plt.savefig(pjoin(output_dir,'Ckwh_ec.png'))


# %%
#Raw entries

df_vis = df_all.reset_index().dropna(subset= ['C_kwh'])
#%%

# tips = [('index','@index'), ('entry source','@source'), ('original name', '@original_name'), ('specific price ($/kg)', '@specific_price'), ('specific energy (kWh/kg)','@specific_energy'), ("price type",'@price_type')]
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
figure.yaxis.axis_label = "Material Energy Cost ($/kWh)"
# show(figure)
figure.yaxis.axis_label_text_font_size = "16pt"
figure.xaxis.major_label_text_font_size = "16pt"

output_file(pjoin(output_dir,'Ckwh_bokeh.html'))
save(figure)