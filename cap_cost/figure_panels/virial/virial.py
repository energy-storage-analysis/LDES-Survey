#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import seaborn as sns

from es_utils.units import read_pint_df
from es_utils.plot import annotate_points

import matplotlib as mpl
plt.rcParams.update({'font.size':12, 'savefig.dpi': 600})
from adjustText import adjust_text

import os
from os.path import join as pjoin
output_dir = 'output'
if not os.path.exists(output_dir): os.makedirs(output_dir)

from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

ADJUST_TEXT_LIM = 5

df = read_pint_df(pjoin(REPO_DIR, 'cap_cost/data_consolidated/SM_data.csv'), index_col=[0,1], drop_units=True).reset_index('SM_type')

CkWh_cases = pd.read_csv(pjoin(REPO_DIR, 'cap_cost','figure_panels','CkWh_cases.csv'), index_col=0)

# %%
df_virial = df.where(df['SM_type'].isin(['flywheel', 'pressure_tank', 'smes'])).dropna(subset=['SM_type'])
df_virial = df_virial.dropna(axis=1, how='all')

df_virial = df_virial.reset_index()

df_virial['SM_name'] = [s.replace('-','').replace('–','') for s in df_virial['SM_name'].values]
df_virial['SM_name'] = [s.replace('StainlessSteel','S.S.') for s in df_virial['SM_name'].values]
df_virial['SM_name'] = [s.replace('CarbonSteel','C.S.') for s in df_virial['SM_name'].values]
df_virial['SM_name'] = [s.replace(' ','\ ') for s in df_virial['SM_name'].values]

df_virial = df_virial.set_index('SM_name')

# %%
df_virial_mat = df_virial.groupby('SM_name').first().drop(['SM_type', 'mu_total', 'Qmax', 'specific_energy', 'C_kwh'], axis=1)

df_virial_mat['specific_strength'] = df_virial_mat['specific_strength']/3600

# energy_densities_line = np.logspace(
#     np.log10(df['specific_energy'].min()),
#     np.log10(df['specific_energy'].max()),
#     )





fig = plt.figure(figsize=(7,6))
sns.scatterplot(data=df_virial_mat, y='specific_price', x='specific_strength', hue='materials')

ax = plt.gca()

texts = annotate_points(df_virial_mat, 'specific_strength','specific_price')

case_lns = []
for case, row in CkWh_cases.iterrows():
    energy_densities_line = np.linspace(3e-3,2)
    mat_cost_line = energy_densities_line*row['value']
    plt.plot(energy_densities_line, mat_cost_line, linestyle=row['linestyle'], color='gray', alpha=0.5)

plt.yscale('log')
plt.xscale('log')

plt.xlabel('Specific Strength (kWh/kg)')
plt.ylabel('Specific Price ($/kg)')

plt.ylim(0.1,100)
plt.xlim(3e-3,2)

lgd = plt.gca().get_legend()
lgd.set_bbox_to_anchor((1, 0.5))

adjust_text(texts, lim=ADJUST_TEXT_LIM, arrowprops = dict(arrowstyle='->'), force_points=(1,1), expand_points=(1.5,1.5), expand_text=(1,1.5))

from es_utils.plot import adjust_text_after

# TODO: make a dict and use this snippet to export a csv file
#
# alter_dict = {
#     "Ba(OH)_{2}/BaO": (1300, 14),
#     # "MgSO_{4}/MgO": (1500,10.3),
# }
# s1 = pd.Series([alter_dict[name][0] for name in alter_dict.keys()], index=alter_dict.keys())
# s1.name = 'x'
# s2 = pd.Series([alter_dict[name][1] for name in alter_dict.keys()], index=alter_dict.keys())
# s2.name = 'y'
# df_out = pd.concat([s1,s2], axis=1)
# df_out.index.name = 'name'
# df_out.to_csv('fix_positions_latent.csv')


# adjust_text_after(fig, ax, "Kevlar", texts, 0.02,30)
# adjust_text_after(fig, ax, "T300PR319", texts, 0.04,20)
# adjust_text_after(fig, ax, "EGlass", texts, 0.04,15)
# adjust_text_after(fig, ax, "AS4/35016", texts, 0.5,10)
# adjust_text_after(fig, ax, "S2\ Glass", texts, 0.1,15)
adjust_text_after(fig, ax, "IM7/8552", texts, 0.82,0.83)
# adjust_text_after(fig, ax, "IM7/85517", texts, 0.45,28)

adjust_text_after(fig, ax, "Steel\ 157", texts, 0.2,.2)
adjust_text_after(fig, ax, "Steel\ 1020", texts, 0.2,.34)

plt.tight_layout()

plt.savefig(pjoin(output_dir,'virial.png'))


# %%
