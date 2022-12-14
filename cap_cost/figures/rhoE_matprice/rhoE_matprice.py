#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
from es_utils.units import read_pint_df

mpl.rcParams.update({'font.size': 16})

import os
from os.path import join as pjoin
output_dir = 'output/Ckwh_line'
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


#Downselect tech for static plots


df_all = df.where(~df['SM_type'].isin([
    # 'gravitational',
    # 'EDLC',
    # 'synfuel',
    # 'dielectric_capacitor',
    # 'pseudocapacitor'
])).dropna(subset=['SM_type'])


# %%


energy_densities_line = np.logspace(
    np.log10(df_all['specific_energy'].min()),
    np.log10(df_all['specific_energy'].max()),
    )

#Mat cost for given C_kwh
mat_cost_line = energy_densities_line*10
#%%

import seaborn as sns
fig = plt.figure(figsize=(8,6))

sns.scatterplot(data=df_all, x='specific_energy', y='specific_price', style='SM_type', hue='SM_type')
plt.xscale('log')
plt.yscale('log')

# plt.xlim(1e-5,1e2)

plt.xlabel('Energy Density (kWh/kg)')
plt.ylabel('Material cost ($/kg)')

plt.plot(energy_densities_line, mat_cost_line, color='gray')

lgd = plt.gca().get_legend()
lgd.set_bbox_to_anchor((1, 1))
# plt.tight_layout()

#https://stackoverflow.com/questions/10101700/moving-matplotlib-legend-outside-of-the-axis-makes-it-cutoff-by-the-figure-box

plt.savefig(pjoin(output_dir,'Ckwh_line.png'), facecolor='white', transparent=False, bbox_extra_artists=(lgd,), bbox_inches='tight')
#%%

df_log = df_all[['specific_price','specific_energy']].apply(np.log10)
# df_log = df_all

df_log['SM_type'] = df_all['SM_type']

df_stats = df_log.groupby('SM_type').agg({
    'specific_price': ['mean','std'],
    'specific_energy': ['mean','std'],
}).sort_values(('specific_energy','mean'),ascending=False)

display_text = pd.read_csv('../tech_lookup.csv', index_col=0)
long_names = [display_text['long_name'][s].replace('\\n','') for s in df_stats.index.values]

df_stats.index = long_names

df_stats

#%%

palette = pd.read_csv('../energy_colors.csv', index_col=0)#['color'].to_dict()
# palette = {key.replace('\\n','\n'): val for key,val in palette.items()}

display_text = pd.read_csv('../tech_lookup.csv')

df_colors = pd.merge(palette, display_text, on='energy_type')
df_colors= df_colors.set_index('long_name')
df_colors.index = [s.replace('\\n','') for s in df_colors.index.values]

color_dict = df_colors['color'].to_dict()

colors = [color_dict[n] for n in df_stats.index]



# #TODO: Improve automatical marker handling
markers = [
            '^','>','<','o','s','x','v',
            'o','x',
            'o',
            'o',
            'P',
            'o',
            'o',
            'x',
            'x',
            'o'
            ]

## Attempt at allowing for different number of SM types automatically
# marker_set = ['o','x','s','^','v','<','>']
# markers = []
# for i in range(len(colors)):
#     markers.append(marker_set[i%len(marker_set)])
#%%

#TODO: The ticks on this figure sometimes only work out correctly in ipython console...

# plt.figure()

fig = plt.figure(figsize=(8,6))

#https://stackoverflow.com/questions/26290493/matplotlib-errorbar-plot-using-a-custom-colormap


cdict = {etype: colors[i] for i, etype in enumerate(df_stats.index)}
mdict = {etype: markers[i] for i, etype in enumerate(df_stats.index)}

for etype, row in df_stats.iterrows():
    plt.scatter(
    x = row['specific_energy']['mean'],
    y = row['specific_price']['mean'],
    c=cdict[etype],
    marker=mdict[etype],
    label=etype
    )

    plt.errorbar(
        x = row['specific_energy']['mean'],
        y = row['specific_price']['mean'],
        xerr = row['specific_energy']['std'],
        yerr = row['specific_price']['std'],
        fmt='none',
        # color='gray',
        c= cdict[etype],
        alpha = 0.5,
        capsize=3

    )

xlim = plt.gca().get_xlim()

energy_densities_line = np.logspace(
    xlim[0] - 1,
    xlim[1] + 1,
    )


mat_cost_line = energy_densities_line*10

mat_cost_line_log = np.log10(mat_cost_line)
energy_densities_line_log = np.log10(energy_densities_line)

plt.plot(energy_densities_line_log, mat_cost_line_log, color='gray')
lgd = plt.legend()


# lgd = plt.gca().get_legend()
lgd.set_bbox_to_anchor((1.08, 1.05))

plt.ylim(-2.5,3.1)
plt.xlim(-3.8,1.8)


from matplotlib.ticker import FuncFormatter

#This is assuming that log tick values are integeers
# TODO: built in way to do this?  
def logformatter10(val, pos):
    return "$10^{" + str(int(val)) + "}$"

formatter = FuncFormatter(logformatter10)

plt.gca().xaxis.set_major_formatter(formatter)
plt.gca().yaxis.set_major_formatter(formatter)

# plt.grid()
plt.xlabel('Energy Density (kWh/kg)')
plt.ylabel('Specific Price ($/kg)')
# plt.xscale('log')

plt.savefig(pjoin(output_dir,'Ckwh_line_errorbar.png'), facecolor='white', transparent=False, bbox_extra_artists=(lgd,), bbox_inches='tight')
# plt.yscale('log')
#%%


# plt.figure()
# SM_types = df_all['SM_type'].value_counts().index
# SM_types

# fig, axes = plt.subplots(1, len(SM_types), figsize=(20,4), sharex=True, sharey=True)

# for i, SM_type in enumerate(SM_types):
#     df_sel = df_all.where(df_all['SM_type'] == SM_type).dropna(how='all')
#     axes[i].scatter(df_sel['specific_energy'], df_sel['specific_price'])
#     axes[i].set_xscale('log')
#     axes[i].set_yscale('log')
#     axes[i].set_title(SM_type)
#     axes[i].set_xlabel('Energy Density \n(kWh/kg)')

#     axes[i].plot(energy_densities_line, mat_cost_line, color='gray')

# axes[0].set_ylabel('Material Cost ($/kg)')

# fig.tight_layout()

# plt.savefig(pjoin(output_dir,'Ckwh_line_separate.png'), facecolor='white', transparent=False,)

#%%

