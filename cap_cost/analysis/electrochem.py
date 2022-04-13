#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

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

df.index = [re.sub('(\d)',r'_\1', s) for s in df.index] #Simple way to format chemical equations as latex. Assumes only time numbers are showing up. 
#%%

df['SM_type'].value_counts()

# %%
df_ec = df.where(df['SM_type'].isin([
'liquid_metal_battery',
'solid_electrode',
'pseudocapacitor',
'flow_battery',
'metal_air',
'hybrid_flow',
'synfuel',
])).dropna(subset=['SM_type'])

df_ec

# %%

# df_latent.plot.scatter(y='C_kwh', x='phase_change_T', c='sp_latent_heat', cmap='jet')
df_ec.plot.scatter(y='C_kwh', x='deltaV')
plt.yscale('log')
plt.xscale('log')
#%%k
df_ec_ds = df_ec.where(df_ec['C_kwh'] < 10).dropna(how='all')

# %%
plt.figure()

x_str='deltaV'
y_str='C_kwh'

import seaborn as sns

sns.scatterplot(data=df_ec_ds, y=y_str, x=x_str, hue='SM_type', legend=True)

ax = plt.gca()
texts = []
for name, row in df_ec_ds.iterrows():
    x = row[x_str]
    y = row[y_str]

    txt= ax.text(x, y, "{}".format(name))
    texts.append(txt)

# plt.xscale('log')

plt.xlabel('Couple Voltage (V)')
plt.ylabel("Material capital cost ($/kWh)")

plt.ylim(0,10)


adjust_text(texts, arrowprops = dict(arrowstyle='->'))

plt.savefig(pjoin(output_dir,'ec.png'))
# %%

