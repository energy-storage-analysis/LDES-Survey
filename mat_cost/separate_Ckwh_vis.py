#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import matplotlib as mpl

mpl.rcParams.update({'font.size': 16})

df_all = pd.read_csv('data/C_kWh.csv', index_col=0)

# df_all = df_all.where(df_all['energy_type'] != 'Electrostatic (Capacitor)').dropna(subset=['energy_type'])

#%%

df_all
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

sns.scatterplot(data=df_all, x='specific_energy', y='specific_price', style='energy_type', hue='energy_type')
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

plt.savefig('output/C_kwh_linefig.png', facecolor='white', transparent=False, bbox_extra_artists=(lgd,), bbox_inches='tight')
#%%

df_log = df_all[['specific_price','specific_energy']].apply(np.log10)
# df_log = df_all

df_log['energy_type'] = df_all['energy_type']

df_stats = df_log.groupby('energy_type').agg({
    'specific_price': ['mean','std'],
    'specific_energy': ['mean','std'],
})

# df_stats = df_stats.apply(np.exp)

df_stats

#%%

#https://stackoverflow.com/questions/26290493/matplotlib-errorbar-plot-using-a-custom-colormap

colors = ["b","g","c","m","y","k","r","g","c","m","y","k"]

cdict = {etype: colors[i] for i, etype in enumerate(df_stats.index)}

for etype, row in df_stats.iterrows():
    plt.scatter(
    x = row['specific_energy']['mean'],
    y = row['specific_price']['mean'],
    c=cdict[etype],
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
mat_cost_line_log = np.log10(mat_cost_line)
energy_densities_line_log = np.log10(energy_densities_line)

plt.plot(energy_densities_line_log, mat_cost_line_log, color='gray')
lgd = plt.legend()


# lgd = plt.gca().get_legend()
lgd.set_bbox_to_anchor((1, 1))


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
plt.ylabel('Material cost ($/kg)')
# plt.xscale('log')

plt.savefig('output/errorbar_agg.png', facecolor='white', transparent=False, bbox_extra_artists=(lgd,), bbox_inches='tight')
# plt.yscale('log')
#%%

energy_types = df_all['energy_type'].value_counts().index
energy_types

fig, axes = plt.subplots(1, len(energy_types), figsize=(20,4), sharex=True, sharey=True)

for i, energy_type in enumerate(energy_types):
    df_sel = df_all.where(df_all['energy_type'] == energy_type).dropna(how='all')
    axes[i].scatter(df_sel['specific_energy'], df_sel['specific_price'])
    axes[i].set_xscale('log')
    axes[i].set_yscale('log')
    axes[i].set_title(energy_type)
    axes[i].set_xlabel('Energy Density \n(kWh/kg)')

    axes[i].plot(energy_densities_line, mat_cost_line, color='gray')

axes[0].set_ylabel('Material Cost ($/kg)')

fig.tight_layout()

plt.savefig('output/C_kwh_linefig_separate.png', facecolor='white', transparent=False,)

#%%

df_sel = df_all.where(df_all['C_kwh'] < 10).dropna(how='all')

df_sel.sort_values('C_kwh').to_csv('output/downselected.csv')