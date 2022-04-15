
#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

mpl.rcParams.update({'font.size':13.5})

import os
from os.path import join as pjoin
output_dir = 'output/eda'
if not os.path.exists(output_dir): os.makedirs(output_dir)
# %%


df_mat_data = pd.read_csv('../data_consolidated/mat_data.csv', index_col=0)
df_SMs = pd.read_csv('../data_consolidated/SM_data.csv', index_col=0)
df_all = pd.read_csv('../data_consolidated/C_kWh.csv', index_col=0)


df_mat_unused = df_mat_data[df_mat_data['num_SMs'] == 0].dropna(how='all')
df_mat_unused.to_csv('output/mat_data_unused.csv')

df_mat_data = df_mat_data[df_mat_data['num_SMs'] > 0].dropna(how='all')
df_mat_data.to_csv('output/mat_data_used.csv')

# %%
plt.figure()

bins = np.logspace(np.log10(0.05), np.log10(2e3), 30)
df_mat_data['specific_price'].hist(bins=bins)

plt.xscale('log')

plt.suptitle("{} Material Prices".format(len(df_mat_data)))
plt.xlabel('Specific Price ($/kg)')

plt.locator_params(axis='y', integer=True)
plt.ylabel('Count')
plt.tight_layout()

plt.savefig(pjoin(output_dir,'eda_mats.png'))


#%%

# plt.figure(figsize=(2,2))
plt.figure(figsize=(5,5))

df_mat_data['num_source'].value_counts().plot.bar()
plt.xlabel("# Sources")
plt.ylabel("Count")

plt.tight_layout()

plt.savefig('output/eda/source_count.png')

#%%

#These datapoints in SM dataset do not have data to calculate C_kwh, when dropping these it is the same length as df_all
missing_idx = [idx for idx in df_SMs.index if idx not in df_all.index.values]
len(missing_idx)

#%%

df_SMs = df_SMs.drop(missing_idx)

#%%

plt.figure()

display_text = pd.read_csv('tech_lookup.csv', index_col=0)
bins = np.logspace(np.log10(1e-4), np.log10(1e2), 30)

df_all['tech_class'] = [display_text['tech_class'][s].replace('\\n','\n') for s in df_all['SM_type'].values]

df_all.groupby('tech_class')['specific_energy'].hist(bins=bins, legend=True, alpha=0.75)

plt.xscale('log')
plt.locator_params(axis='y', integer=True)
plt.suptitle("{} Storage Media".format(len(df_all)))
plt.xlabel('Energy Density (kWh/kg)')
plt.ylabel('Count')
plt.tight_layout()


plt.savefig('output/eda/SM_energy.png')

#%%

# df_all = df_all.dropna(subset=['C_kwh'])

#%%
#Has both price and energy data


df_both = df_all.dropna(subset = ['C_kwh'])

plt.figure()

bins = np.logspace(np.log10(1e-3), np.log10(1e6), 50)

df_both.groupby('tech_class')['C_kwh'].hist(bins=bins, legend=True, alpha=0.75)

plt.xscale('log')
plt.suptitle("{} Storage Media w/ Mat. Prices".format(len(df_both)))
plt.xlabel('Material Captial Cost ($/kWh)')
plt.ylabel('Count')

plt.gca().get_legend().remove()

plt.savefig(pjoin(output_dir,'SM_w_prices.png'))
