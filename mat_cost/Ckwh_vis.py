#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

prices = pd.read_csv('data/prices_molecular.csv', index_col=0)
sp_energy = pd.read_csv('data/sp_energy_molecular.csv', index_col=0)

prices = prices.dropna(subset=['specific_price_element'])


sp_energy = sp_energy.where(sp_energy['molecular_formula_norm'] != 'O3U').dropna(how='all')
sp_energy

# %%
prices['specific_price_avg'] = sum([prices['specific_price_refs'].fillna(0),
prices['specific_price_UI'].fillna(0),
prices['specific_price_element'].fillna(0)])/3


prices


#%%
sp_energy
# %%

df_vis = sp_energy[['molecular_formula_norm', 'energy_type', 'specific_energy']]


df_vis['specific_price_avg'] = prices['specific_price_avg'].loc[sp_energy['molecular_formula_norm']].values

df_vis['C_kwh'] = df_vis['specific_price_avg']/df_vis['specific_energy']

df_vis


#%%
cat_label = 'energy_type'

from matplotlib import ticker as mticker
plt.rcParams.update({'font.size': 20})

df_vis['C_kwh_log'] = np.log10(df_vis['C_kwh'])

fig = plt.figure(figsize = (13,6))
# plt.violinplot(dataset=df_all['C_kwh'].values)
# sns.violinplot(data=df_all, x='cat_label', y='C_kwh_log')
sns.stripplot(data=df_vis, x=cat_label, y='C_kwh_log', size=10)

plt.axhline(np.log10(10), linestyle='--', color='gray')

fig.axes[0].yaxis.set_major_formatter(mticker.StrMethodFormatter("$10^{{{x:.0f}}}$"))
fig.axes[0].yaxis.set_ticks([np.log10(x) for p in range(-1,4) for x in np.linspace(10**p, 10**(p+1), 10)], minor=True)
# plt.gca().set_xticks(np.arange(0, len(labels)), labels=labels)

# plt.yscale('log')
plt.xticks(rotation=45)
plt.ylabel('Material Energy Cost ($/kWh)')
# %%



# %%
sp_energy['molecular_formula_norm']

#%%
df_e = sp_energy[['molecular_formula_norm', 'energy_type', 'specific_energy']]
df_e = df_e.set_index('molecular_formula_norm')
df_e

#%%
df_prices_refs = prices['specific_price_refs'].dropna().rename('specific_price').to_frame()
df_prices_refs['price_type']= 'reference'
df_prices_UI = prices['specific_price_UI'].dropna().rename('specific_price').to_frame()
df_prices_UI['price_type']= 'USGS/ISE'
df_prices_element = prices['specific_price_element'].dropna().rename('specific_price').to_frame()
df_prices_element['price_type']= 'elemental'


df_prices_2 = pd.concat([
    df_prices_refs,
    df_prices_UI,
    df_prices_element
])

# df_prices_2 = df_prices_2.reset_index()

df_prices_2

#Downselect to those preset
df_prices_2 = df_prices_2.loc[set(df_e.index)]

df_prices_2

#%%

df_vis = pd.merge(df_prices_2, df_e, on='molecular_formula_norm')

df_vis['C_kwh'] = df_vis['specific_price']/df_vis['specific_energy']

df_vis.to_csv('data/combined.csv')
df_vis
# %%
cat_label = 'energy_type'

from matplotlib import ticker as mticker
plt.rcParams.update({'font.size': 20})

df_vis['C_kwh_log'] = np.log10(df_vis['C_kwh'])

fig = plt.figure(figsize = (13,6))
# plt.violinplot(dataset=df_all['C_kwh'].values)
# sns.violinplot(data=df_all, x='cat_label', y='C_kwh_log')
sns.stripplot(data=df_vis, x=cat_label, y='C_kwh_log', hue='price_type', size=10)

plt.axhline(np.log10(10), linestyle='--', color='gray')

fig.axes[0].yaxis.set_major_formatter(mticker.StrMethodFormatter("$10^{{{x:.0f}}}$"))
fig.axes[0].yaxis.set_ticks([np.log10(x) for p in range(-1,4) for x in np.linspace(10**p, 10**(p+1), 10)], minor=True)
# plt.gca().set_xticks(np.arange(0, len(labels)), labels=labels)

# plt.yscale('log')
plt.xticks(rotation=45)
plt.ylabel('Material Energy Cost ($/kWh)')
# %%

plt.savefig('output/fig_C_kwh.png')

# %%
