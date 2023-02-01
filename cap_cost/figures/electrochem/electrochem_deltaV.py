#%%
import os
from os.path import join as pjoin
import pandas as pd
import matplotlib.pyplot as plt
import re
import seaborn as sns

from es_utils.units import read_pint_df
from es_utils.plot import annotate_points

import matplotlib as mpl
plt.rcParams.update({'font.size':12, 'savefig.dpi': 600})
from adjustText import adjust_text

from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

output_dir = 'output'
if not os.path.exists(output_dir): os.makedirs(output_dir)

df = read_pint_df(pjoin(REPO_DIR,'cap_cost/data_consolidated/SM_data.csv'), index_col=[0,1], drop_units=True).reset_index('SM_type')

df.index = [re.sub('(\D)(\d)(\D|$)',r'\1_\2\3', s) for s in df.index] #Simple way to format chemical equations as latex. Assumes only time numbers are showing up. 

df['SM_type'] = df['SM_type'].replace('liquid_metal_battery', 'liquid_metal')

#Calculate deltaV for synfuels
F = 96485 # C/mol
df_ec_synfuel = df[df['SM_type'] == 'synfuel'].dropna(subset=['SM_type'])
deltaV_synfuel = (df_ec_synfuel['deltaG_chem']*3600000)/(F*df_ec_synfuel['n_e'])
df.loc[deltaV_synfuel.index,'deltaV'] = deltaV_synfuel


# %%
df_ec_coupled = df.where(df['SM_type'].isin([
'liquid_metal',
'solid_electrode',
'metal_air',
'hybrid_flow',
])).dropna(subset=['SM_type'])

df_ec_coupled = df_ec_coupled.where(df_ec_coupled['C_kwh'] < 10).dropna(how='all')


df_ec_decoupled = df.where(df['SM_type'].isin([
'flow_battery',
'synfuel'
])).dropna(subset=['SM_type'])

df_ec_decoupled = df_ec_decoupled.where(df_ec_decoupled['C_kwh'] < 10).dropna(how='all')
# %%
plt.figure(figsize = (7,5))

x_str='deltaV'
y_str='C_kwh'

sns.scatterplot(data=df_ec_coupled, y=y_str, x=x_str, hue='SM_type', legend=True)

ax = plt.gca()


texts = annotate_points(df_ec_coupled, x_str, y_str, ax=ax)

# plt.xscale('log')
ax.set_title('Coupled')

plt.xlabel('Couple Voltage (V)')
plt.ylabel("$C_{kWh,mat}$ (\$/kWh)")

# plt.ylim(0,10)
plt.ylim(1e-1,20)
plt.yscale('log')

# plt.xlim(0,5.5)

adjust_text(texts, arrowprops = dict(arrowstyle='->'), force_points=(0.2,1))

plt.savefig(pjoin(output_dir,'ec_coupled.png'))


#%%

plt.figure(figsize = (5,5))

sns.scatterplot(data=df_ec_decoupled, y=y_str, x=x_str, hue='SM_type', legend=True)

ax = plt.gca()

df_ec_decoupled['display_text'] = [s.replace(" ", r"\ ") for s in df_ec_decoupled.index]
texts = annotate_points(df_ec_decoupled, x_str, y_str, 'display_text', ax=ax)

ax.set_title('Decoupled')


# plt.ylim(0,10)
plt.ylim(2e-4,20)
plt.yscale('log')

plt.gca().get_legend().set_bbox_to_anchor([0,0.6,0.5,0])

adjust_text(texts, arrowprops = dict(arrowstyle='->'))

plt.xlabel('Couple Voltage (V)')
plt.ylabel("$C_{kWh,mat}$ (\$/kWh)")

plt.savefig(pjoin(output_dir,'ec_decoupled.png'))


# %%

df_nofeedstock = df_ec_decoupled.loc[['Feedstock' not in idx for idx in df_ec_decoupled.index]]

plt.figure(figsize = (5,5))

sns.scatterplot(data=df_nofeedstock, y=y_str, x=x_str, hue='SM_type', legend=True)

ax = plt.gca()

df_nofeedstock['display_text'] = [s.replace(" ", r"\ ") for s in df_nofeedstock.index]
texts = annotate_points(df_nofeedstock, x_str, y_str, 'display_text', ax=ax)

ax.set_title('Decoupled')

# plt.ylim(0,10)
plt.ylim(1e-2,20)
plt.xlim(0.6,1.6)
plt.yscale('log')

# plt.hlines(0.01, 1,2)

plt.gca().get_legend().set_bbox_to_anchor([0,0.4,0.5,0])

adjust_text(texts, arrowprops = dict(arrowstyle='->'))

plt.xlabel('Couple Voltage (V)')
plt.ylabel("$C_{kWh,mat}$ (\$/kWh)")

plt.tight_layout()

plt.savefig(pjoin(output_dir,'ec_decoupled_nofeedstock.png'))
