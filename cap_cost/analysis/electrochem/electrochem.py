#%%
import os
from os.path import join as pjoin
import pandas as pd
import matplotlib.pyplot as plt
import re
import seaborn as sns
from es_utils.units import read_pint_df

import matplotlib as mpl
mpl.rcParams.update({'font.size':12})
from adjustText import adjust_text

from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

output_dir = 'output'
if not os.path.exists(output_dir): os.makedirs(output_dir)

df = read_pint_df(pjoin(REPO_DIR,'cap_cost/data_consolidated/SM_data.csv'), index_col=[0,1], drop_units=True).reset_index('SM_type')

df.index = [re.sub('(\D)(\d)(\D|$)',r'\1_\2\3', s) for s in df.index] #Simple way to format chemical equations as latex. Assumes only time numbers are showing up. 

df['SM_type'] = df['SM_type'].replace('liquid_metal_battery', 'liquid_metal')

# %%
df_ec = df.where(df['SM_type'].isin([
'liquid_metal',
'solid_electrode',
# 'pseudocapacitor', #Doesn't have delta V...
'flow_battery',
'metal_air',
'hybrid_flow',
# 'synfuel', #Doesn't have delta V....
])).dropna(subset=['SM_type'])

df_ec_ds = df_ec.where(df_ec['C_kwh'] < 10).dropna(how='all')

# %%
plt.figure(figsize = (8,5))

x_str='deltaV'
y_str='C_kwh'

sns.scatterplot(data=df_ec_ds, y=y_str, x=x_str, hue='SM_type', legend=True)

ax = plt.gca()
texts = []
for name, row in df_ec_ds.iterrows():
    x = row[x_str]
    y = row[y_str]

    txt= ax.text(x, y, "${}$".format(name))
    texts.append(txt)

# plt.xscale('log')

plt.xlabel('Couple Voltage (V)')
plt.ylabel("$C_{kWh,mat}$ (\$/kWh)")

# plt.ylim(0,10)
plt.ylim(2e-1,20)
plt.yscale('log')

# adjust_text(texts, arrowprops = dict(arrowstyle='->'))

plt.savefig(pjoin(output_dir,'ec.png'))

#%%

F = 96485 # C/mol

df_ec_synfuel = df[df['SM_type'] == 'synfuel'].dropna(subset=['SM_type'])
df_ec_synfuel['deltaV'] = (df_ec_synfuel['deltaG_chem']*3600000)/(F*df_ec_synfuel['n_e'])

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
])).dropna(subset=['SM_type'])

df_ec_decoupled = pd.concat([
    df_ec_decoupled,
    df_ec_synfuel,
    # df_ec_fossil
])

df_ec_decoupled = df_ec_decoupled.where(df_ec_decoupled['C_kwh'] < 10).dropna(how='all')
# %%
plt.figure(figsize = (7,5))

x_str='deltaV'
y_str='C_kwh'

sns.scatterplot(data=df_ec_coupled, y=y_str, x=x_str, hue='SM_type', legend=True)

ax = plt.gca()
texts = []
for name, row in df_ec_coupled.iterrows():
    x = row[x_str]
    y = row[y_str]

    txt= ax.text(x, y, "${}$".format(name))
    texts.append(txt)

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

x_str='deltaV'
y_str='C_kwh'

sns.scatterplot(data=df_ec_decoupled, y=y_str, x=x_str, hue='SM_type', legend=True)

ax = plt.gca()
texts = []
for name, row in df_ec_decoupled.iterrows():
    x = row[x_str]
    y = row[y_str]

    name = name.replace(" ", r"\ ")
    txt= ax.text(x, y, "${}$".format(name))
    texts.append(txt)

# plt.xscale('log')

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

x_str='deltaV'
y_str='C_kwh'

sns.scatterplot(data=df_nofeedstock, y=y_str, x=x_str, hue='SM_type', legend=True)

ax = plt.gca()
texts = []
for name, row in df_nofeedstock.iterrows():
    x = row[x_str]
    y = row[y_str]

    name = name.replace(" ", r"\ ")
    txt= ax.text(x, y, "${}$".format(name))
    texts.append(txt)

# plt.xscale('log')

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


# %%

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
texts = []
for name, row in df_plot.iterrows():
    x = row[x_str]
    y = row[y_str]

    txt= ax.text(x, y, "${}$".format(name))
    texts.append(txt)

# plt.xscale('log')
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
