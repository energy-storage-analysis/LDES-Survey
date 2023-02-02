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

### Flow 

df_ec_coupled = df.where(df['SM_type'].isin([
'hybrid_flow',
])).dropna(subset=['SM_type'])

df_ec_decoupled = df.where(df['SM_type'].isin([
'flow_battery',
])).dropna(subset=['SM_type'])

df = pd.concat([df_ec_coupled, df_ec_decoupled])

# df_plot = df.where(df['C_kwh'] < 10).dropna(how='all')
df_plot = df
# %%
plt.figure(figsize = (7,5))

x_str='deltaV'
y_str='C_kwh'

sns.scatterplot(data=df_plot, y=y_str, x=x_str, hue='SM_type', legend=True)

ax = plt.gca()

texts = annotate_points(df_plot, x_str,y_str,ax=ax)

ax.set_title('Coupled')

plt.xlabel('Couple Voltage (V)')
plt.ylabel("$C_{kWh,mat}$ (\$/kWh)")

# plt.ylim(0,10)
# plt.ylim(1e-1,20)
plt.yscale('log')

# plt.xlim(0,5.5)

adjust_text(texts, arrowprops = dict(arrowstyle='->'), force_points=(0.2,1))

plt.savefig(pjoin(output_dir,'ec_flow_all.png'))

# %%
