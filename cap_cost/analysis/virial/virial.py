#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import seaborn as sns

from es_utils.units import read_pint_df
from es_utils.plot import annotate_points

import matplotlib as mpl
mpl.rcParams.update({'font.size':12})
from adjustText import adjust_text

import os
from os.path import join as pjoin
output_dir = 'output'
if not os.path.exists(output_dir): os.makedirs(output_dir)

from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

df = read_pint_df(pjoin(REPO_DIR, 'cap_cost/data_consolidated/SM_data.csv'), index_col=[0,1], drop_units=True).reset_index('SM_type')



# %%
df_virial = df.where(df['SM_type'].isin(['flywheel', 'pressure_tank', 'smes'])).dropna(subset=['SM_type'])
df_virial = df_virial.dropna(axis=1, how='all')

df_virial = df_virial.reset_index()

df_virial['SM_name'] = [s.replace('-','').replace('–','') for s in df_virial['SM_name'].values]
df_virial['SM_name'] = [s.replace('StainlessSteel','S.S.') for s in df_virial['SM_name'].values]
df_virial['SM_name'] = [s.replace('CarbonSteel','C.S.') for s in df_virial['SM_name'].values]

df_virial = df_virial.set_index('SM_name')

df_virial

# %%
df_virial_mat = df_virial.groupby('SM_name').first().drop(['SM_type', 'T_min', 'mu_total', 'Qmax', 'specific_energy', 'C_kwh'], axis=1)

df_virial_mat['specific_strength'] = df_virial_mat['specific_strength']/3600

# energy_densities_line = np.logspace(
#     np.log10(df['specific_energy'].min()),
#     np.log10(df['specific_energy'].max()),
#     )

energy_densities_line = np.linspace(1e-2,2)
mat_cost_line = energy_densities_line*10

plt.figure()
sns.scatterplot(data=df_virial_mat, y='specific_price', x='specific_strength', hue='materials')

ax = plt.gca()

texts = annotate_points(df_virial_mat, 'specific_strength','specific_price')

plt.plot(energy_densities_line, mat_cost_line)

plt.yscale('log')
plt.xscale('log')

plt.xlabel('Specific Strength (kWh/kg)')
plt.ylabel('Specific Price ($/kg)')

plt.ylim(0.5,100)
plt.xlim(5e-3,2)

lgd = plt.gca().get_legend()
lgd.set_bbox_to_anchor((1, 1))

adjust_text(texts,  arrowprops = dict(arrowstyle='->'), force_points=(0.2,3))

plt.tight_layout()

plt.savefig(pjoin(output_dir,'virial.png'))


# %%
