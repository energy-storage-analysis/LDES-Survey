#%%
import os
from os.path import join as pjoin
import pandas as pd
import matplotlib.pyplot as plt
import re
import seaborn as sns

from es_utils.units import read_pint_df
from es_utils.plot import annotate_points
from es_utils.chem import format_chem_formula

import matplotlib as mpl
mpl.rcParams.update({'font.size':12})
label_fontsize = 14
ADJUST_TEXT_LIM = 5

from adjustText import adjust_text

from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

output_dir = 'output'
if not os.path.exists(output_dir): os.makedirs(output_dir)

df = read_pint_df(pjoin(REPO_DIR,'cap_cost/data_consolidated/SM_data.csv'), index_col=[0,1], drop_units=True).reset_index('SM_type')


formula_strings = [format_chem_formula(s) for s in df.index]
df['display_text'] = formula_strings


df['SM_type'] = df['SM_type'].replace('liquid_metal_battery', 'liquid_metal')

Ckwh_cutoff = 30
y_max = Ckwh_cutoff*1.15

#%%

df_ec_synfuel = df.where(df['SM_type'].isin([
'synfuel'
])).dropna(subset=['SM_type'])

df_ec_synfuel['SM_type'] = df_ec_synfuel['SM_type'] + "\n(" + df_ec_synfuel['sub_type'] + ")"


df_ec_decoupled = df.where(df['SM_type'].isin([
'flow_battery',
])).dropna(subset=['SM_type'])

df_ec_decoupled = pd.concat([
df_ec_synfuel,
df_ec_decoupled
])


# %%
df_ec_coupled = df.where(df['SM_type'].isin([
'liquid_metal',
'solid_electrode',
'metal_air',
'hybrid_flow',
])).dropna(subset=['SM_type'])

df_ec_coupled = df_ec_coupled.where(df_ec_coupled['C_kwh'] < Ckwh_cutoff).dropna(how='all')
df_ec_decoupled = df_ec_decoupled.where(df_ec_decoupled['C_kwh'] < Ckwh_cutoff).dropna(how='all')

df_ec_coupled.dropna(axis=1, how='all').to_csv(pjoin(output_dir,'SM_coupled_ds.csv'))
df_ec_decoupled.dropna(axis=1, how='all').to_csv(pjoin(output_dir,'SM_decoupled_ds.csv'))



# %%
print("Coupled")

plt.figure(figsize = (7,8))

x_str='specific_energy'
y_str='C_kwh'

sns.scatterplot(data=df_ec_coupled, y=y_str, x=x_str, hue='SM_type', legend=True, s=50)

ax = plt.gca()
ax.hlines(10,ax.get_xlim()[0],ax.get_xlim()[1]*1.1, linestyle='--', color='gray')

texts = annotate_points(df_ec_coupled, x_str, y_str, text_col='display_text', ax=ax)

ax.set_title('Coupled')
plt.xlabel('Specific Energy (kWh/kg)', fontsize=label_fontsize)
plt.ylabel("$C_{kWh,mat}$ (\$/kWh)", fontsize=label_fontsize)

plt.yscale('log')
plt.xscale('log')
plt.ylim(top=y_max)
plt.xlim(2e-2,2e1)


leg = ax.get_legend()
leg.set_title('')
leg.set_bbox_to_anchor([0,0.3,0.4,0])

adjust_text(texts, arrowprops = dict(arrowstyle='->'), force_points=(10,0.5), lim=ADJUST_TEXT_LIM)

plt.savefig(pjoin(output_dir,'ec_rhoE_coupled.png'))


#%%

print("Decoupled")
plt.figure(figsize = (7,8))

sns.scatterplot(data=df_ec_decoupled, y=y_str, x=x_str, hue='SM_type', legend=True, s=50)

ax = plt.gca()
ax.hlines(10,ax.get_xlim()[0],ax.get_xlim()[1]*1.1, linestyle='--', color='gray')

texts = annotate_points(df_ec_decoupled, x_str, y_str, 'display_text', ax=ax)

plt.yscale('log')
plt.xscale('log')
plt.ylim(bottom=5e-3, top=y_max)

# plt.gca().get_legend().set_bbox_to_anchor([0,0.6,0.5,0])

ax.set_title('Decoupled')
plt.xlabel('Specific Energy (kWh/kg)', fontsize=label_fontsize)
plt.ylabel("$C_{kWh,mat}$ (\$/kWh)", fontsize=label_fontsize)

adjust_text(texts, arrowprops = dict(arrowstyle='->'), force_points=(1,1), lim=ADJUST_TEXT_LIM)
leg = ax.get_legend()
leg.set_title('')
leg.set_bbox_to_anchor([0,0,0.6,0.45])


plt.savefig(pjoin(output_dir,'ec_rhoE_decoupled.png'))

# %%
