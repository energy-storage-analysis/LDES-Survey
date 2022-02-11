#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import seaborn as sns
sys.path.append('..')

# Alva Thermal
df_latent = pd.read_csv('alva/output/table_8.csv', index_col=0)

df_latent['C_kwh'] = df_latent['cost']/(df_latent['sp_latent_heat'])

df_4 = pd.read_csv('alva/output/table_4.csv', index_col=0)
df_5 = pd.read_csv('alva/output/table_5.csv', index_col=0)
df_6 = pd.read_csv('alva/output/table_6.csv', index_col=0)
df_7 = pd.read_csv('alva/output/table_7.csv', index_col=0)

col_sel = ['Cp', 'kth', 'cost', 'class']


df_sens = pd.concat([df[col_sel] for df in [df_4, df_5, df_6, df_7]])

df_sens['Cp'] = df_sens['Cp'].astype(float)
df_sens['Cp'] = df_sens['Cp']/3600

df_sens['kth'] = df_sens['kth'].astype(float)

# df_sens['cost'] = df_sens['cost'].str.replace(',','.')
df_sens['cost'] = df_sens['cost'].astype(float)

df_sens['C_kwh'] = df_sens['cost']/(df_sens['Cp']*500)

df_sens


#%%
df_ec = pd.read_csv('li_2017/output/table_2.csv', index_col=0)
df_ec


#%%

df_virial = pd.read_csv('nomura_2017/table_2_mat.csv', index_col=0)

df_virial['specific_energy'] = (1*df_virial['max stress'])/df_virial['density']
df_virial['specific_energy'] = df_virial['specific_energy']/3600000
df_virial['C_kwh'] = df_virial['mat_cost']/df_virial['specific_energy']

df_virial

#%%

from kale_2018.vis import load_tables

kale_tables = load_tables('kale_2018')

# %%

s_latent = df_latent['C_kwh'].dropna()
s_sens = df_sens['C_kwh'].dropna()
s_ec = df_ec['C_kwh'].dropna()
s_virial_metal = kale_tables['a1']['C_kwh'].dropna()
s_virial_comp = kale_tables['a2']['C_kwh'].dropna()

dataset = [
    s_latent.values,
    s_sens.values,
    s_ec.values,
    s_virial_metal.values,
    s_virial_comp.values
]

labels=[
    'Latent Thermal \n(Alva et al 2018)', 
    'Sensible Thermal (deltaT = 500K)\n(Alva et al 2018)',
    'Chemical (electrochemical)\n(Li et al 2017)',
    'Viral (metals)\n(Kale et al. 2018)', 
    'Viral (composites)\n(Kale et al. 2018)'
    ]

plt.figure(figsize = (15,6))
plt.violinplot(dataset=dataset, positions=range(len(dataset)))
sns.stripplot(data=dataset)

plt.axhline(10, linestyle='--', color='gray')

plt.gca().set_xticks(np.arange(0, len(labels)), labels=labels)

plt.yscale('log')
# plt.xticks(rotation=90)
plt.ylabel('Material Energy Cost ($/kWh)')
# %%
