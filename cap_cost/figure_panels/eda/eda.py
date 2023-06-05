
#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
from es_utils.units import read_pint_df
# plt.rcParams.update({'font.size':16, 'savefig.dpi': 600})

plt.rcParams.update({
    "savefig.facecolor": 'white',
    "font.size": 7, 
    'savefig.dpi': 600, 
    'font.sans-serif': 'arial', 
    'figure.figsize': (2.3, 1.6)
})

grid = False


import os
from os.path import join as pjoin
output_dir = 'output'
if not os.path.exists(output_dir): os.makedirs(output_dir)

from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

palette = pd.read_csv('../energy_colors.csv', index_col=0)['color'].to_dict()
palette = {key.replace('\\n','\n'): val for key,val in palette.items()}

# %%

df_SMs = read_pint_df(pjoin(REPO_DIR,'cap_cost/data_consolidated/SM_data.csv'), index_col=[0,1], drop_units=True).reset_index('SM_type')
df_mat_data = read_pint_df(pjoin(REPO_DIR, 'cap_cost/data_consolidated/mat_data.csv'), index_col=0, drop_units=True)

df_mat_data = df_mat_data[df_mat_data['num_SMs'] > 0] 

# %%
plt.figure()

bins = np.logspace(np.log10(0.05), np.log10(2e3), 30)
df_mat_data['specific_price'].hist(
    bins=bins, 
    color='slategray', 
    grid=grid
    )

plt.xscale('log')

# plt.suptitle("{} Material Prices".format(len(df_mat_data))) #Used in at least one storage medium
plt.xlabel('Specific Price (USD/kg)')

plt.locator_params(axis='y', integer=True)
plt.ylabel('Count')
plt.ylim(0,18)

plt.xticks([10.0**x for x in np.arange(-1,4)])

plt.tight_layout()

plt.savefig(pjoin(output_dir,'eda_mats.png'))


#%%


plt.figure(figsize=(1.35,0.9))
# plt.figure(figsize=(5,5))

df_plot = df_mat_data['num_source'].value_counts().sort_index()


max_number = 6

count_above_max = df_plot.where(df_plot.index > max_number).dropna().sum()

df_plot = df_plot.where(df_plot.index <= max_number).dropna()
df_plot.index = df_plot.index.astype(str)

df_plot.loc['>{}'.format(max_number)] = count_above_max

df_plot.plot.bar(color='slategray')
plt.xlabel("# Sources")
plt.ylabel("Count")

plt.xticks(rotation=0)
plt.yticks([0,20,40])

plt.tight_layout()

#TODO: Cannot figure out how to have axes patch white but axis transparent without ipython. Going to manually put white background in svg...
# plt.gca().patch.set_alpha(0)
# plt.gcf().set_alpha(0)
plt.savefig(pjoin(output_dir,'source_count.png'), facecolor='none')
# plt.savefig(pjoin(output_dir,'source_count.png'), transparent=True)

#%%

df_SMs = df_SMs.dropna(subset=['C_kwh'])

#%%

plt.figure()

display_text = pd.read_csv('../tech_lookup.csv', index_col=0)
bins = np.logspace(np.log10(2e-4), np.log10(5e1), 30)

df_SMs['energy_type'] = [display_text['energy_type'][s].replace('\\n','\n') for s in df_SMs['SM_type'].values]

for energy_type, color in palette.items():
    df_sel = df_SMs[df_SMs['energy_type'] == energy_type].dropna(how='all')
    df_sel['specific_energy'].hist(
        bins=bins, 
        label=energy_type, 
        alpha=1, 
        color=color, 
        grid=grid,
        )


plt.xscale('log')
plt.locator_params(axis='y', integer=True)
# plt.suptitle("{} Storage Media".format(len(df_SMs)))
plt.xlabel('Energy Density (kWh/kg)')
plt.ylabel('Count')

# plt.yscale('log')
plt.ylim(top=39)
# leg= plt.legend(title='Energy Type', loc='upper left')

plt.xticks([10.0**x for x in np.arange(-3,2)])

plt.tight_layout()


plt.savefig(pjoin(output_dir,'SM_energy.png'))

