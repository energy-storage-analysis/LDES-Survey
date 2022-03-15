#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import matplotlib as mpl

mpl.rcParams.update({'font.size': 16})

df_prices = pd.read_csv('data/df_prices.csv', index_col=0)

df_singlemat = pd.read_csv('data/df_singlemat.csv', index_col=0) 
df_singlemat = df_singlemat.dropna(subset=['specific_energy'])

df_couples = pd.read_csv('data/df_couples.csv', index_col=0) 

#%%
col_select = ['energy_type', 'specific_energy','specific_price', 'source', 'original_name','price_type']

df_all = pd.concat([
    df_singlemat[col_select],
    df_couples[col_select]
]) 

df_all['C_kwh'] = df_all['specific_price']/df_all['specific_energy']

df_all = df_all.dropna(subset=['C_kwh'])

df_all = df_all.where(df_all['energy_type'] != 'electrostatic').dropna(subset=['energy_type'])

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
fig = plt.figure(figsize=(10,6))

sns.scatterplot(data=df_all, x='specific_energy', y='specific_price', style='energy_type', hue='energy_type')
plt.xscale('log')
plt.yscale('log')
# plt.gca().get_legend().set_bbox_to_anchor([0,0,1.6,1])

plt.xlabel('Energy Density (kWh/kg)')
plt.ylabel('Material cost ($/kg)')

plt.plot(energy_densities_line, mat_cost_line, color='gray')

# plt.tight_layout()

plt.savefig('output/C_kwh_linefig.png', facecolor='white', transparent=False,)
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