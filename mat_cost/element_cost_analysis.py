#%%

import chemparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os


dataset_folder = '../datasets'

element_prices = pd.read_csv(
    os.path.join(dataset_folder, r'wiki_element_cost\output\process.csv')
    , index_col=1)

def calculate_formula_price(chemparse_dict):
    total_price = 0
    total_mass = 0
    for atom, num in chemparse_dict.items():
        if atom in element_prices.index:

            row = element_prices.loc[atom]
            
            kg_per_mol = row['molar_mass']/1000

            total_mass += kg_per_mol*num #kg/mol

            cost_per_mol = row['cost']*kg_per_mol
            total_price += cost_per_mol*num   #$/mol 
        else:
            return np.nan

    price = total_price/total_mass #$/kg

    return price


#%%
df_tc = pd.read_csv('pdf/andre_2016/output/process.csv')

df_tc = df_tc.rename({'reactant':'chemical_name'}, axis=1)

df_tc['formula_dict'] = df_tc['chemical_name'].apply(chemparse.parse_formula)

df_tc['element_price'] = df_tc['formula_dict'].apply(calculate_formula_price)

df_tc['C_kwh_element'] = df_tc['element_price']/df_tc['specific_energy']

df_tc.sort_values('C_kwh_element')
# %%
df_latent = pd.read_csv('pdf/alva_2018/output/latent.csv')

df_latent = df_latent.rename({'name':'chemical_name', 'C_kwh':'C_kwh_orig'}, axis=1)

df_latent['formula_dict'] = df_latent['chemical_name'].apply(chemparse.parse_formula)

df_latent['element_price'] = df_latent['formula_dict'].apply(calculate_formula_price)

df_latent['C_kwh_element'] = df_latent['element_price']/df_latent['sp_latent_heat']

df_latent.sort_values('C_kwh_element')
# %%

# df_ec = pd.read_csv('pdf/li_2017/output/process.csv')

# df_ec = df_ec.dropna(subset=['chemical'])

# df_ec['formula_dict'] = df_ec['chemical'].apply(chemparse.parse_formula)
# df_ec


#%%
cols = ['C_kwh','cat_label','chemical_name']


df_latent_element = df_latent.rename({'C_kwh_element': 'C_kwh'}, axis=1)
df_latent_element['cat_label'] = 'Latent (element)'
df_latent_orig = df_latent.rename({'C_kwh_orig': 'C_kwh'}, axis=1)
df_latent_orig['cat_label'] = 'Latent (Original)'

df_tc_element = df_tc.rename({'C_kwh_element': 'C_kwh'}, axis=1)
df_tc_element['cat_label'] ='Thermochemical (element)'

df_all = pd.concat([
df_tc_element[cols].dropna().reset_index(drop=True),
df_latent_element[cols].dropna().reset_index(drop=True),
df_latent_orig[cols].dropna().reset_index(drop=True),
])

from matplotlib import ticker as mticker
plt.rcParams.update({'font.size': 20})

df_all['C_kwh_log'] = np.log10(df_all['C_kwh'])

fig = plt.figure(figsize = (13,6))
# plt.violinplot(dataset=df_all['C_kwh'].values)
# sns.violinplot(data=df_all, x='cat_label', y='C_kwh_log')
sns.stripplot(data=df_all, x='cat_label', y='C_kwh_log', size=10)

plt.axhline(np.log10(10), linestyle='--', color='gray')

fig.axes[0].yaxis.set_major_formatter(mticker.StrMethodFormatter("$10^{{{x:.0f}}}$"))
fig.axes[0].yaxis.set_ticks([np.log10(x) for p in range(-1,4) for x in np.linspace(10**p, 10**(p+1), 10)], minor=True)
# plt.gca().set_xticks(np.arange(0, len(labels)), labels=labels)

# plt.yscale('log')
plt.xticks(rotation=45)
plt.ylabel('Material Energy Cost ($/kWh)')
# %%
