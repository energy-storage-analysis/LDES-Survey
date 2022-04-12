#%%
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#%%

tables = {fn.strip('.csv') : pd.read_csv(os.path.join('output',fn), index_col=0) for fn in os.listdir('output')}

df = pd.concat(tables)


df['specific_energy'] = df['specific_energy'].astype(float)
df['enthalpy'] = df['enthalpy'].astype(float)
df['temperature'] = df['temperature'].astype(float)

df['enthalpy'] = df['enthalpy']/3600 #kJ to kWh
df['specific_energy'] = df['specific_energy']/3600 #kJ to kWh


df
# %%


# bins = np.logspace(np.log10(0.1), np.log10(1e6), 50)
# bins = np.linspace(100,3000, 50)

df.groupby('type')['specific_energy'].hist(legend=True, alpha=0.5)

plt.xlabel('Gravimetric Energy (kWh/kg)')
plt.ylabel('count')

# %%

df.groupby('type')['enthalpy'].hist(legend=True, alpha=0.5)

plt.xlabel('Molar enthalpy (kWh/mol)')
plt.ylabel('count')
#%%

df.groupby('type')['temperature'].hist(legend=True, alpha=0.5)

plt.xlabel('Temperature')
plt.ylabel('count')
# %%

# %%
