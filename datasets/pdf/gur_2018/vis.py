#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import sys

import es_utils

df = pd.read_csv('output/table_10.csv')

df = es_utils.concat_row_to_columns(df, 3)
df = df.drop('0 1 2', axis=1)

df = df.rename(
    {
    'Materials  ': 'material', 
    'Melting Point  (oC)': 'melting_point', 
    'Thermal Conductivity (W/m.K)': 'therm_cond',
    'Density  (kg/m3)': 'density',
    'Specific Heat, Cp (J/kg.K)': 'Cp',
    'Vol. Energy Density (kJ/m3)': 'energy_density'
       },
axis=1)

df = df.dropna(subset= ['density'])
#%%
bins = np.logspace(np.log10(1e-1), np.log10(1e2), num=30)
df['Cp'].hist(bins=bins)
plt.xscale('log')
#%%

bins = np.logspace(np.log10(1e2), np.log10(1e4), num=30)
df['energy_density'].astype(float).hist(bins=bins)
plt.xscale('log')

# %%
