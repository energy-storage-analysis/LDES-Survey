#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import seaborn as sns

import matplotlib as mpl
mpl.rcParams.update({'font.size':12})
from adjustText import adjust_text

import os
from os.path import join as pjoin
output_dir = 'output/single_tech'
if not os.path.exists(output_dir): os.makedirs(output_dir)

df_SM = pd.read_csv('../data_consolidated/SM_data.csv', index_col=[0,1])
df = df_SM.reset_index('SM_type')

df.index = [re.sub('(\D)(\d)(\D|$)',r'\1_\2\3', s) for s in df.index] #Simple way to format chemical equations as latex. Assumes only time numbers are showing up. 

df['SM_type'] = df['SM_type'].replace('liquid_metal_battery', 'liquid_metal')
#%%

df['SM_type'].value_counts()

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

df_ec


#%%


# df_latent.plot.scatter(y='C_kwh', x='phase_change_T', c='sp_latent_heat', cmap='jet')
df_ec.plot.scatter(y='C_kwh', x='deltaV')
plt.yscale('log')
plt.xscale('log')
#%%k
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
plt.ylabel("Material Energy Cost ($/kWh)")

# plt.ylim(0,10)
plt.ylim(2e-1,20)
plt.yscale('log')

adjust_text(texts, arrowprops = dict(arrowstyle='->'))

plt.savefig(pjoin(output_dir,'ec.png'))
# %%

#%%

df_ec_synfuel = df[df['SM_type'] == 'synfuel'].dropna(subset=['SM_type'])
df_ec_synfuel

#TODO: this molar mass is what was used in calculating deltaG, should probably just have deltaG be specified per mol and energy density caluclated with total molar mass. But have to redo how total molar mass is caluclated because the specific price for synthetic fuels is calcualted on a mass basis.
# df_ec_synfuel['mu_product'] = [16,2,2,32]
# df_ec_synfuel['mu_product'] = df_ec_synfuel['mu_product']/1000 #kg/mol

#%%

F = 96485 # C/mol
df_ec_synfuel['deltaV'] = (df_ec_synfuel['deltaG_chem']*3600000)/(F*df_ec_synfuel['n_e'])
df_ec_synfuel['deltaV']

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
    df_ec_synfuel
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
plt.ylabel("Material Energy Cost ($/kWh)")

# plt.ylim(0,10)
plt.ylim(1e-1,20)
plt.yscale('log')

# plt.xlim(0,5.5)

adjust_text(texts, arrowprops = dict(arrowstyle='->'), force_points=(0.2,1))

plt.savefig(pjoin(output_dir,'ec_coupled.png'))


#%%

plt.figure(figsize = (4,5))

x_str='deltaV'
y_str='C_kwh'

sns.scatterplot(data=df_ec_decoupled, y=y_str, x=x_str, hue='SM_type', legend=True)

ax = plt.gca()
texts = []
for name, row in df_ec_decoupled.iterrows():
    x = row[x_str]
    y = row[y_str]

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
plt.ylabel("Material Energy Cost ($/kWh)")

plt.savefig(pjoin(output_dir,'ec_decoupled.png'))


# %%

df_nofeedstock = df_ec_decoupled.loc[['Feedstock' not in idx for idx in df_ec_decoupled.index]]

plt.figure(figsize = (4,5))

x_str='deltaV'
y_str='C_kwh'

sns.scatterplot(data=df_nofeedstock, y=y_str, x=x_str, hue='SM_type', legend=True)

ax = plt.gca()
texts = []
for name, row in df_nofeedstock.iterrows():
    x = row[x_str]
    y = row[y_str]

    txt= ax.text(x, y, "${}$".format(name))
    texts.append(txt)

# plt.xscale('log')

ax.set_title('Decoupled')

# plt.ylim(0,10)
plt.ylim(1e-1,20)
plt.yscale('log')


# plt.gca().get_legend().set_bbox_to_anchor([0,0.6,0.5,0])

adjust_text(texts, arrowprops = dict(arrowstyle='->'))

plt.xlabel('Couple Voltage (V)')
plt.ylabel("Material Energy Cost ($/kWh)")

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
plt.ylabel("Material Energy Cost ($/kWh)")

# plt.ylim(0,10)
# plt.ylim(1e-1,20)
plt.yscale('log')

# plt.xlim(0,5.5)

adjust_text(texts, arrowprops = dict(arrowstyle='->'), force_points=(0.2,1))

plt.savefig(pjoin(output_dir,'ec_flow_all.png'))
