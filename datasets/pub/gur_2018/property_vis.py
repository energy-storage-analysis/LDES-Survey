#%%
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pint_pandas

df_thermal = pd.read_csv('data/Gur_thermal.csv', index_col=[0], skiprows=[1])

# df_thermal = pd.read_csv('data/Gur_thermal.csv', header=[0,1], index_col=[0])
# type = df_thermal.pop('Type')
# df_thermal = df_thermal.pint.quantify(level=1)
# df_thermal['Type'] = type
# df_thermal

#%%

bins = np.linspace(0,5000, num = 20)

df_thermal.groupby('Type')['Cp'].hist(bins=bins, legend=True)
plt.xlabel('Specific Heat (J/kg K)')
plt.ylabel('Count')

#%%

Cp_nowater = df_thermal['Cp'].drop(['ethylene glycol-water','Water'])
sens = Cp_nowater*500/3600
sens.hist()
plt.xlabel('Stored Energy at 500K (Wh/kg)')

# %%

df_thermal = pd.read_csv('data/Gur_latent.csv', index_col=0, skiprows=[1])

df_thermal
#%%
df_thermal['Enthalpy of Fusion']
# %%
bins = np.linspace(0,0.6, num = 20)
df_thermal['Enthalpy of Fusion'].hist(bins=bins)

# %%
