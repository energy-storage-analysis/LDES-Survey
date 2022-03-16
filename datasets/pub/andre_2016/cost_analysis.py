"""Attempt to use USGS/ISE data for $/kWh of thermochemical materials"""

#%%

import pandas as pd
import numpy as np
import ast
import os 

import sys




usgs_folder = r'C:\Users\aspit\Git\MHDLab-Projects\Energy-Storage-Analysis\pdf_data\usgs\output'
ise_folder = r'C:\Users\aspit\Git\MHDLab-Projects\Energy-Storage-Analysis\pdf_data\ISE\output'

df_ise_chem = pd.read_csv(os.path.join(ise_folder, 'ISE_chem_data.csv'), index_col=0)



# %%
df_usgs_chem = pd.read_csv(os.path.join(usgs_folder, 'chem_data.csv'), index_col=1)

df_usgs = pd.read_csv(os.path.join(usgs_folder, 'prices_proc_edit.csv'), index_col=0)
avg_price = df_usgs.groupby('chemical')['specific_price'].mean()

df_usgs = pd.concat([
    df_usgs_chem['pubchem_top_formula'],
    avg_price,
], axis=1).dropna(subset=['pubchem_top_formula'])

df_usgs

#%%

df_ise_chem = pd.read_csv(os.path.join(ise_folder, 'ISE_chem_data.csv'), index_col=1)

df_ise = pd.read_csv(os.path.join(ise_folder, 'ISE_proc_edit.csv'), index_col=0)
avg_price = df_ise.groupby('chemical')['specific_price'].mean()

df_ise = pd.concat([
    df_ise_chem['pubchem_top_formula'],
    avg_price,
], axis=1).dropna(subset=['pubchem_top_formula'])

df_ise

# %%


df['reactant_norm'] = [normalize_formula(s) for s in df.index]
df['product_norm'] = [normalize_formula(s) for s in df['product']]
df

# %%

# df.apply(normalize_formula)
# %%

price_data_chems = list(set([
    *df_ise['pubchem_top_formula'],
    *df_usgs['pubchem_top_formula']
]))

thermochemical_all = list(set([
    *df['reactant_norm'],
    *df['product_norm']
]))


for chem in price_data_chems:
    if chem in thermochemical_all:
        print(chem)
