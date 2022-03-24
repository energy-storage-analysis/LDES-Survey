#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df_SM = pd.read_csv('data/SM_data.csv', index_col=0)
df_Ckwh = pd.read_csv('data/C_kwh.csv', index_col=0)

common_columns = [c for c in df_SM.columns if c in df_Ckwh.columns]

df_SM = df_SM.drop(common_columns, axis=1)

# %%
df = pd.concat([df_SM, df_Ckwh], axis=1)

df.info()

#%%

df['SM_type'].value_counts()

# %%
df_latent = df.where(df['SM_type'] == 'latent_thermal').dropna(subset=['SM_type'])

df_latent = df_latent.dropna(axis=1, how='all')

df_latent.info()

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
for name, row in df_latent_ds.iterrows():
    x = row['phase_change_T']
    y = row['sp_latent_heat']
    name = name.split(' ')[0]

    if x > 1200:
        x = x-100
        y = y+0.005
    else:
        x = x+50

    if y > 0.2:
        y = y
    else:
        y = y+0.001

    if name == 'Si/Mg/Ca':
        y = y - 0.005

    ax.annotate(name, (x,y))

plt.yscale('log')
# %%


plt.figure()
df_latent_ds.plot.scatter(y='C_kwh', x='phase_change_T', c='sp_latent_heat', cmap='viridis', sharex=False)


ax = plt.gca()
for name, row in df_latent_ds.iterrows():
    x = row['phase_change_T']
    y = row['C_kwh']
    name = name.split(' ')[0]

    if x > 1200:
        x = x-100
    else:
        x = x+50

    ax.annotate(name, (x,y))

plt.yscale('log')

plt.xlabel('Phase Change Temperature (K)')
plt.ylabel("Material capital cost ($/kWh)")

plt.savefig('ds_output/latent.png')
# %%
df_sens = df.where(df['SM_type'] == 'sensible_thermal').dropna(subset=['SM_type'])

df_sens = df_sens.dropna(axis=1, how='all')

df_sens.info()
# %%

# df_latent.plot.scatter(y='C_kwh', x='phase_change_T', c='sp_latent_heat', cmap='jet')
df_sens.plot.scatter(y='C_kwh', x='kth')
plt.yscale('log')
plt.xscale('log')
#%%k
df_sens_ds = df_sens.where(df_sens['C_kwh'] < 10).dropna(how='all')

# %%
plt.figure()

x_str='kth'
y_str='C_kwh'

df_sens_ds.plot.scatter(y=y_str, x=x_str, c='Cp', cmap='viridis', sharex=False)


ax = plt.gca()
for name, row in df_sens_ds.iterrows():
    x = row[x_str]
    y = row[y_str]
    name = name[0:24]

    
    if x > 1:
        x = x-np.log(x*1.2)
        y=y+ 0.1

    if name=='Quartzite':
        y = y +0.1
    # else:
    #     x = x+50

    ax.annotate(name, (x,y))

# plt.yscale('log')
plt.xscale('log')

plt.xlabel('Thermal Conductivity (W/m/K)')
plt.ylabel("Material capital cost ($/kWh)")

plt.savefig('ds_output/sensible.png')
# %%
