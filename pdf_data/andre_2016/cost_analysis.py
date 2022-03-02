"""Attempt to use USGS/ISE data for $/kWh of thermochemical materials"""

#%%

import pandas as pd
import numpy as np
import ast
import os 

import sys

sys.path.append(r'C:\Users\aspit\Git\MHDLab-Projects\Energy Storage Analysis\mat2vec')
from mat2vec.processing import MaterialsTextProcessor


mat_processor = MaterialsTextProcessor()
def normalize_formula(s):
    if s != None:
        return mat_processor.process(s)[0][0]
    else: 
        return None


usgs_folder = r'C:\Users\aspit\Git\MHDLab-Projects\Energy Storage Analysis\pdf_data\usgs\output'
ise_folder = r'C:\Users\aspit\Git\MHDLab-Projects\Energy Storage Analysis\pdf_data\ISE\output'

df_usgs_chem = pd.read_csv(os.path.join(usgs_folder, 'chem_data.csv'), index_col=0)
df_ise_chem = pd.read_csv(os.path.join(ise_folder, 'ISE_chem_data.csv'), index_col=0)



# %%
df_usgs = pd.read_csv(os.path.join(usgs_folder, 'prices_proc_edit.csv'), index_col=0)
avg_price = df_usgs.groupby('chemical')['price_per_kg'].mean()

df_usgs = pd.concat([
    df_usgs_chem['norm_formula'],
    avg_price,
], axis=1).dropna(subset=['norm_formula'])

#%%

df_ise = pd.read_csv(os.path.join(ise_folder, 'ISE_proc_edit.csv'), index_col=0)
avg_price = df_ise.groupby('chemical')['price_per_kg'].mean()

df_ise = pd.concat([
    df_ise_chem['norm_formula'],
    avg_price,
], axis=1).dropna(subset=['norm_formula'])


df_ise


# %%
tables = {fn.strip('.csv') : pd.read_csv(os.path.join('output',fn), index_col=0) for fn in os.listdir('output')}

df = pd.concat(tables.values())


df['specific_energy'] = df['specific_energy'].astype(float)
df['enthalpy'] = df['enthalpy'].astype(float)
df['temperature'] = df['temperature'].astype(float)

df['enthalpy'] = df['enthalpy']/3600 #kJ to kWh
df['specific_energy'] = df['specific_energy']/3600 #kJ to kWh

df['reactant_norm'] = [normalize_formula(s) for s in df.index]
df['product_norm'] = [normalize_formula(s) for s in df['product']]
df

# %%

# df.apply(normalize_formula)
# %%

for f in df['reactant_norm']:
    if f in df_usgs['norm_formula']:
        print(f)

for f in df['product_norm']:
    if f in df_usgs['norm_formula']:
        print(f)
# %%

for f in df['reactant_norm']:
    if f in df_ise['norm_formula']:
        print(f)

for f in df['product_norm']:
    if f in df_ise['norm_formula']:
        print(f)