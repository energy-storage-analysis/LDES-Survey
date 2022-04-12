#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

from adjustText import adjust_text

df_SM = pd.read_csv('data_consolidated/SM_data.csv', index_col=[0,1])
df_Ckwh = pd.read_csv('data_consolidated/C_kwh.csv', index_col=[0,1])

common_columns = [c for c in df_SM.columns if c in df_Ckwh.columns]

df_SM = df_SM.drop(common_columns, axis=1)

# %%
df = pd.concat([df_SM, df_Ckwh], axis=1)

df = df.reset_index('SM_type')


df.index = [re.sub('(\d)',r'_\1', s) for s in df.index] #Simple way to format chemical equations as latex. Assumes only time numbers are showing up. 
#%%

df['SM_type'].value_counts()

# %%
df_latent = df.where(df['SM_type'] == 'latent_thermal').dropna(subset=['SM_type'])

df_latent = df_latent.dropna(axis=1, how='all')


#%%

# df_latent.plot.scatter(y='C_kwh', x='phase_change_T', c='sp_latent_heat', cmap='jet')
df_latent.plot.scatter(y='C_kwh', x='phase_change_T')
plt.yscale('log')
# %%

df_latent_ds = df_latent.where(df_latent['C_kwh'] < 10).dropna(how='all')

#This drops Boron, with phase change > 2000
df_latent_ds = df_latent_ds.where(df_latent['phase_change_T'] < 2000).dropna(how='all')

df_latent_ds.plot.scatter(y='sp_latent_heat', x='phase_change_T', c='C_kwh', cmap='jet', sharex=False)


ax = plt.gca()
texts = []
for name, row in df_latent_ds.iterrows():
    x = row['phase_change_T']
    y = row['sp_latent_heat']
    name = name.split(' ')[0]

    txt = ax.text(x, y, "${}$".format(name))
    texts.append(txt)

plt.yscale('log')
adjust_text(texts)
# %%


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
plt.ylim(0.8,10)

plt.xlabel('Phase Change Temperature (K)')
plt.ylabel("Material capital cost ($/kWh)")

plt.gcf().axes[1].set_ylabel('Specific Latent Heat (kWh/kg)')

adjust_text(texts)

plt.savefig('results/specific_tech/latent.png')
# %%
df_sens = df.where(df['SM_type'] == 'sensible_thermal').dropna(subset=['SM_type'])

df_sens = df_sens.dropna(axis=1, how='all')

# %%

# df_latent.plot.scatter(y='C_kwh', x='phase_change_T', c='sp_latent_heat', cmap='jet')
df_sens.plot.scatter(y='C_kwh', x='kth')
plt.yscale('log')
plt.xscale('log')
#%%k
df_sens_ds = df_sens.where(df_sens['C_kwh'] < 10).dropna(how='all')

# %%
plt.figure()

#TODO: LINaKCO3 appears to not have measured thermal conductivity data
x_str='kth'
y_str='C_kwh'

#TODO: https://www.researchgate.net/publication/252121179_Thermal_Conductivity_of_Magnetite_and_Hematite
df_sens_ds.loc['Iron Ore','kth'] = 5

df_sens_ds.plot.scatter(y=y_str, x=x_str, c='Cp', cmap='jet', sharex=False)


ax = plt.gca()
texts = []
for name, row in df_sens_ds.iterrows():
    x = row[x_str]
    y = row[y_str]
    name = name[0:25]

    txt= ax.text(x, y, "${}$".format(name))
    texts.append(txt)

# plt.yscale('log')
plt.xscale('log')

plt.xlabel('Thermal Conductivity (W/m/K)')
plt.ylabel("Material capital cost ($/kWh)")

plt.ylim(0,5)

plt.gcf().axes[1].set_ylabel('Specific heat (kWh/K/kg)')

adjust_text(texts)

plt.savefig('results/specific_tech/sensible.png')
# %%


df_tc = df.where(df['SM_type'] == 'thermochemical').dropna(subset=['SM_type'])
df_tc = df_tc.dropna(axis=1,how='all')


df_tc = df_tc.where(df_tc['C_kwh'] < 10).dropna(how='all')

df_tc

#%%
import seaborn as sns

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
plt.gca().get_legend().set_bbox_to_anchor([0,0,1.3,1])
plt.yscale('log')
plt.xlabel('Reaction Temperature (C)')
plt.ylabel("Material capital cost ($/kWh)")
plt.tight_layout()

adjust_text(texts, arrowprops = dict(arrowstyle='->'))


plt.savefig('results/specific_tech/thermochem.png')
# %%
