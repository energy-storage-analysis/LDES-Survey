
#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
from es_utils.units import read_pint_df

mpl.rcParams.update({'font.size':13.5})

import os
from os.path import join as pjoin
output_dir = 'output/eda'
if not os.path.exists(output_dir): os.makedirs(output_dir)


palette = pd.read_csv('energy_colors.csv', index_col=0)['color'].to_dict()
palette = {key.replace('\\n','\n'): val for key,val in palette.items()}

# %%

df_SMs = read_pint_df('../data_consolidated/SM_data.csv', index_col=[0,1], drop_units=True).reset_index('SM_type')
df_mat_data = read_pint_df('../data_consolidated/mat_data.csv', index_col=0, drop_units=True)

df_mat_unused = df_mat_data[df_mat_data['num_SMs'] == 0].dropna(how='all')
df_mat_unused.to_csv('output/mat_data_unused.csv')

df_mat_data = df_mat_data[df_mat_data['num_SMs'] > 0].dropna(how='all')
df_mat_data.to_csv('output/mat_data_used.csv')

# %%
plt.figure(figsize=(7,5))

bins = np.logspace(np.log10(0.05), np.log10(5e2), 30)
df_mat_data['specific_price'].hist(bins=bins)

plt.xscale('log')

plt.suptitle("{} Material Prices used in at least 1 storage medium".format(len(df_mat_data)))
plt.xlabel('Median Specific Price ($/kg)')

plt.locator_params(axis='y', integer=True)
plt.ylabel('Count')
plt.tight_layout()
plt.ylim(0,10)

plt.savefig(pjoin(output_dir,'eda_mats.png'))


#%%

plt.figure(figsize=(2.5,2))
# plt.figure(figsize=(5,5))

df_mat_data['num_source'].value_counts().plot.bar()
plt.xlabel("# Sources")
plt.ylabel("Count")

plt.tight_layout()

plt.savefig('output/eda/source_count.png')

#%%

df_SMs = df_SMs.dropna(subset=['C_kwh'])

#%%

plt.figure(figsize=(7,5))

display_text = pd.read_csv('tech_lookup.csv', index_col=0)
bins = np.logspace(np.log10(2e-4), np.log10(1e2), 30)

df_SMs['energy_type'] = [display_text['energy_type'][s].replace('\\n','\n') for s in df_SMs['SM_type'].values]

# df_SMs.groupby('energy_type')['specific_energy'].hist(bins=bins, legend=True, alpha=0.75)

for energy_type, color in palette.items():
    df_sel = df_SMs[df_SMs['energy_type'] == energy_type].dropna(how='all')
    df_sel['specific_energy'].hist(bins=bins, label=energy_type, alpha=0.75, color=color)


plt.xscale('log')
plt.legend()
plt.locator_params(axis='y', integer=True)
plt.suptitle("{} Storage Media".format(len(df_SMs)))
plt.xlabel('Energy Density (kWh/kg)')
plt.ylabel('Count')
plt.tight_layout()


plt.savefig('output/eda/SM_energy.png')

#%%

# df_SMs = df_SMs.dropna(subset=['C_kwh'])

#%%
#Has both price and energy data


df_both = df_SMs.dropna(subset = ['C_kwh'])

plt.figure()

bins = np.logspace(np.log10(1e-3), np.log10(1e6), 50)

df_both.groupby('energy_type')['C_kwh'].hist(bins=bins, legend=True, alpha=0.75)

plt.xscale('log')
plt.suptitle("{} Storage Media w/ Mat. Prices".format(len(df_both)))
plt.xlabel('Material Captial Cost ($/kWh)')
plt.ylabel('Count')

plt.gca().get_legend().remove()

plt.savefig(pjoin(output_dir,'SM_w_prices.png'))
