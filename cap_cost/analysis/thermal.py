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
df_Ckwh = pd.read_csv('../data_consolidated/C_kwh.csv', index_col=[0,1])

common_columns = [c for c in df_SM.columns if c in df_Ckwh.columns]

df_SM = df_SM.drop(common_columns, axis=1)

df = pd.concat([df_SM, df_Ckwh], axis=1)
df = df.reset_index('SM_type')
df.index = [re.sub('(\D)(\d)(\D|$)',r'\1_\2\3', s) for s in df.index] #Simple way to format chemical equations as latex. Assumes only time numbers are showing up. 

# %%
df_latent = df.where(df['SM_type'] == 'latent_thermal').dropna(subset=['SM_type'])
df_latent = df_latent.dropna(axis=1, how='all')
df_latent_ds = df_latent.where(df_latent['C_kwh'] < 10).dropna(how='all')

#This drops Boron, with phase change > 2000
df_latent_ds = df_latent_ds.where(df_latent['phase_change_T'] < 2000).dropna(how='all')

plt.figure()
df_latent_ds.plot.scatter(y='C_kwh', x='phase_change_T', c='sp_latent_heat', cmap='jet', sharex=False)


ax = plt.gca()
texts = []
for name, row in df_latent_ds.iterrows():
    x = row['phase_change_T']
    y = row['C_kwh']
    name = name.split(' ')[0]

    txt = ax.text(x, y, "${}$".format(name))
    texts.append(txt)


plt.yscale('log')
plt.ylim(0.05,20)
# plt.ylim(0,10)
plt.xlim(500,1500)

plt.xlabel('Phase Change Temperature (deg C)')
plt.ylabel("Material Energy Cost ($/kWh)")

plt.gcf().axes[1].set_ylabel('Specific Latent Heat (kWh/kg)')

adjust_text(texts,  arrowprops = dict(arrowstyle='->'), force_points=(5,10))

plt.savefig(pjoin(output_dir,'latent.png'))
# %%
df_sens = df.where(df['SM_type'] == 'sensible_thermal').dropna(subset=['SM_type'])
df_sens = df_sens.dropna(axis=1, how='all')
df_sens = df_sens.rename({'Vegetable Oil': 'Veg. Oil'})

df_sens_ds = df_sens.where(df_sens['C_kwh'] < 10).dropna(how='all')


plt.figure()

x_str='T_max'
y_str='C_kwh'

df_sens_ds.plot.scatter(y=y_str, x=x_str, c='deltaT', cmap='jet', sharex=False)

ax = plt.gca()
texts = []
for name, row in df_sens_ds.iterrows():
    x = row[x_str]
    y = row[y_str]
    # name = name[0:25].replace('_','') #TODO: error when adding steinmann...

    txt= ax.text(x, y, "${}$".format(name))
    texts.append(txt)

# plt.xscale('log')
plt.yscale('log')
plt.ylim(0.05,20)
# plt.ylim(0,10)

plt.xlim(-500,3550)

plt.xlabel('Maximum Temperature (deg C)')
plt.ylabel("Material Energy Cost ($/kWh)")


plt.gcf().axes[1].set_ylabel('Maximum DeltaT (deg C)')

adjust_text(texts,  arrowprops = dict(arrowstyle='->'), force_points=(5,2))

plt.savefig(pjoin(output_dir,'sensible.png'))
# %%


df_tc = df.where(df['SM_type'] == 'thermochemical').dropna(subset=['SM_type'])
df_tc = df_tc.dropna(axis=1,how='all')
df_tc = df_tc.where(df_tc['C_kwh'] < 10).dropna(how='all')

plt.figure()
x_str='temperature'
y_str='C_kwh'

sns.scatterplot(data=df_tc, y=y_str, x=x_str, hue='type', legend=True)

ax = plt.gca()
texts = []
for name, row in df_tc.iterrows():
    x = row[x_str]
    y = row[y_str]
    # name = row['materials']

    txt = ax.text(x,y,"${}$".format(name))
    texts.append(txt)

plt.xlim(0,2000)
# plt.gca().get_legend().set_bbox_to_anchor([0,0,1.3,1])

plt.yscale('log')
plt.ylim(0.05,20)
# plt.ylim(0,10)

plt.xlabel('Reaction Temperature (C)')
plt.ylabel("Material Energy Cost ($/kWh)")
plt.tight_layout()

adjust_text(texts, arrowprops = dict(arrowstyle='->'), force_points=(0,5))

plt.savefig(pjoin(output_dir,'thermochem.png'))
# %%
