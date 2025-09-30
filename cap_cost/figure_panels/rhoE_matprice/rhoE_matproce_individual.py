#%%
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd
import numpy as np
from os.path import join as pjoin

from es_utils.units import read_pint_df

import matplotlib as mpl
plt.rcParams.update({'font.size':12, 'savefig.dpi': 600})
label_fontsize = 14
from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

output_dir = 'output'
if not os.path.exists(output_dir): os.makedirs(output_dir)

CkWh_cases = pd.read_csv(pjoin(REPO_DIR, 'cap_cost','figure_panels','CkWh_cases.csv'), index_col=0)
Ckwh_cutoff = CkWh_cases['value']['MDES']
# Ckwh_cutoff = 100
y_lim = (0.1, Ckwh_cutoff*2)

df = read_pint_df(pjoin(REPO_DIR,'cap_cost/data_consolidated/SM_data.csv'), index_col=[0,1], drop_units=True).reset_index('SM_type')

df['SM_type'] = df['SM_type'].str.replace('_',' ').str.title()
df['sub_type'] = df['sub_type'].str.replace('_',' ').str.title()
df['mat_type'] = df['mat_type'].str.replace('_',' ').str.title()

#%%
df_latent = df.where(df['SM_type'] == 'Latent Thermal').dropna(subset=['SM_type'])
df_latent = df_latent.dropna(axis=1, how='all')
df_latent_ds = df_latent.where(df_latent['C_kwh'] <Ckwh_cutoff).dropna(how='all')

#%%
df_latent.plot(x='sp_latent_heat', y='specific_price', kind='scatter', figsize=(4,3))

plt.xlim(1e-3, 1e1)
plt.ylim(1e-2, 1e2)

plt.xscale('log')
plt.yscale('log')

plt.xlabel('$\Delta H_{f} \ [kWh/kg]$')
plt.ylabel('Specific Price [$/kg]')

xlim = plt.xlim()

energy_densities_line = np.linspace(
    xlim[0] - 1,
    xlim[1] + 1,
    )

case_lns = []
for case, row in CkWh_cases.iterrows():
    mat_cost_line = energy_densities_line*row['value']
    plt.plot(energy_densities_line, mat_cost_line, color='gray', linestyle=row['linestyle'], alpha=0.5)


plt.savefig(pjoin(output_dir,'latent_heat_vs_specific_price.png'), bbox_inches='tight')
#%%

df_thermochem = df.where(df['SM_type'] == 'Thermochemical').dropna(subset=['SM_type'])
df_thermochem = df_thermochem.dropna(axis=1, how='all')
df_thermochem_ds = df_thermochem.where(df_thermochem['C_kwh'] <Ckwh_cutoff).dropna(how='all')   

#%%

df_thermochem.plot(x='deltaH_thermochem', y='specific_price', kind='scatter', figsize=(4,3))

plt.xlim(1e-3, 1e1)
plt.ylim(2e-2, 2e2)

plt.xscale('log')
plt.yscale('log')

xlim = plt.xlim()

energy_densities_line = np.linspace(
    xlim[0] - 1,
    xlim[1] + 1,
    )

case_lns = []
for case, row in CkWh_cases.iterrows():
    mat_cost_line = energy_densities_line*row['value']
    plt.plot(energy_densities_line, mat_cost_line, color='gray', linestyle=row['linestyle'], alpha=0.5)


plt.xlabel('$\Delta H_{rxn} \ [kWh/kg]$')
plt.ylabel('Specific Price [$/kg]')

plt.savefig(pjoin(output_dir,'thermochem_vs_specific_price.png'), bbox_inches='tight')
# %%

df_sensible = df.where(df['SM_type'] == 'Sensible Thermal').dropna(subset=['SM_type'])
df_sensible = df_sensible.dropna(axis=1, how='all')
df_sensible_ds = df_sensible.where(df_sensible['C_kwh'] <Ckwh_cutoff).dropna(how='all')   

#%%

df_sensible.plot(x='specific_energy', y='specific_price', kind='scatter', figsize=(3,2.5))

plt.xlim(1e-4, 1e2)
plt.ylim(2e-4, 2e2)

plt.xscale('log')
plt.yscale('log')

xlim = plt.xlim()

energy_densities_line = np.linspace(
    xlim[0] - 1,
    xlim[1] + 1,
    )

case_lns = []
for case, row in CkWh_cases.iterrows():
    mat_cost_line = energy_densities_line*row['value']
    plt.plot(energy_densities_line, mat_cost_line, color='gray', linestyle=row['linestyle'], alpha=0.5)


plt.xlabel('$\\rho_E \ [kWh/kg]$')
plt.ylabel('Specific Price [$/kg]')

plt.savefig(pjoin(output_dir,'sensible_vs_specific_price.png'), bbox_inches='tight')

# %%