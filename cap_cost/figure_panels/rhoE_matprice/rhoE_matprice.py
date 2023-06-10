#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from es_utils.units import read_pint_df
plt.rcParams.update({'font.size':16, 'savefig.dpi': 600})

import os
from os.path import join as pjoin
output_dir = 'output'
if not os.path.exists(output_dir): os.makedirs(output_dir)

from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')


CkWh_cases = pd.read_csv(pjoin(REPO_DIR, 'cap_cost','figure_panels','CkWh_cases.csv'), index_col=0)

df = read_pint_df(pjoin(REPO_DIR, 'cap_cost/data_consolidated/SM_data.csv'), index_col=[0,1], drop_units=True).reset_index('SM_type')
#%%
# %%
#Downselect tech for static plots


df_all = df.where(~df['SM_type'].isin([
    # 'gravitational',
    # 'EDLC',
    # 'synfuel',
    # 'dielectric_capacitor',
    # 'pseudocapacitor'
])).dropna(subset=['SM_type'])




energy_densities_line = np.logspace(
    np.log10(df_all['specific_energy'].min()),
    np.log10(df_all['specific_energy'].max()),
    )

#Mat cost for given C_kwh
# mat_cost_line = energy_densities_line*10


display_text = pd.read_csv('../tech_lookup.csv', index_col=0)

df_all['SM_type'] = df_all['SM_type'].str.replace("(","\n(", regex=False)

df_all['display_text'] = [display_text['long_name'][s].replace('\\n','\n') for s in df_all['SM_type'].values]

#%%

import seaborn as sns
fig = plt.figure(figsize=(8,6))

sns.scatterplot(data=df_all, x='specific_energy', y='specific_price', style='display_text', hue='display_text')
plt.xscale('log')
plt.yscale('log')

# plt.xlim(1e-5,1e2)

plt.xlabel('Energy Density (kWh/kg)')
plt.ylabel('Material cost ($/kg)')

case_lns = []
for case, row in CkWh_cases.iterrows():
    # energy_densities_line = np.linspace(1e-2,2)
    mat_cost_line = energy_densities_line*row['value']
    plt.plot(energy_densities_line, mat_cost_line, linestyle=row['linestyle'], color='gray', alpha=0.5)

lgd = plt.gca().get_legend()
lgd.set_bbox_to_anchor((1, 1))
lgd.set_title('Technology')
# plt.tight_layout()

#https://stackoverflow.com/questions/10101700/moving-matplotlib-legend-outside-of-the-axis-makes-it-cutoff-by-the-figure-box

plt.savefig(pjoin(output_dir,'rhoE_matprice_points.png'), facecolor='white', transparent=False, bbox_extra_artists=(lgd,), bbox_inches='tight')
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



case_lns = []
for case, row in CkWh_cases.iterrows():
    # energy_densities_line = np.linspace(1e-2,2)
    mat_cost_line = energy_densities_line*row['value']
    # plt.plot(energy_densities_line, mat_cost_line, linestyle=row['linestyle'], color='gray', alpha=0.5)



    mat_cost_line_log = np.log10(mat_cost_line)
    energy_densities_line_log = np.log10(energy_densities_line)

    plt.plot(energy_densities_line_log, mat_cost_line_log, color='gray', linestyle=row['linestyle'])


# lgd = plt.gca().get_legend()

#TODO: Make these based on the min an max of standard deviation
plt.ylim(-2,4.5)
plt.xlim(-6.5,1.3)


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

#TODO: Can't bring this legend in closer horizontally without being placed above the figure
lgd = plt.legend()
lgd.set_bbox_to_anchor((1.15, 1))

plt.savefig(pjoin(output_dir,'Ckwh_line_errorbar.png'), facecolor='white', transparent=False, bbox_extra_artists=(lgd,), bbox_inches='tight')
# plt.yscale('log')
