#%%
import os
from os.path import join as pjoin
import numpy as np
import pandas as pd
from es_utils import join_col_vals

dataset_folder = '../datasets'
dataset_index = pd.read_csv(pjoin(dataset_folder,'dataset_index.csv'), index_col=0)

# col_select = ['material_name', 'molecular_formula', 'original_name','specific_price','specific_energy','energy_type','source']
dfs_price = []
dfs_physprop = []

for source, row in dataset_index.iterrows():
    fp_prices = os.path.join(dataset_folder, row['folder'], 'output', 'mat_prices.csv')
    if os.path.exists(fp_prices):
        df_price = pd.read_csv(fp_prices,index_col=0)

        #Custom data dataset already has source column
        if source != 'custom_data':
            df_price['source'] = source

        dfs_price.append(df_price)

    fp_physprop = os.path.join(dataset_folder, row['folder'], 'output', 'physprop.csv')
    if os.path.exists(fp_physprop):
        df_price = pd.read_csv(fp_physprop,index_col=0)

        #Custom data dataset already has source column
        if source != 'custom_data':
            df_price['source'] = source

        dfs_physprop.append(df_price)
    

df_prices = pd.concat(dfs_price)
df_physprop = pd.concat(dfs_physprop)

# df.index.name = 'index'

#%%

df_physprop.to_csv('data/physprops.csv')

## Collect prices 

#%%


s_temp = df_prices.groupby('index').apply(join_col_vals, column='source')
s_temp.name = 'source'
df_prices_combine = s_temp.to_frame()

df_prices_combine['num_source'] = df_prices_combine['source'].str.split(',').apply(len)
df_prices_combine['specific_price_refs'] = df_prices.groupby('index')['specific_price'].mean()

# df_prices['specific_energy'] = df.groupby('index')['specific_energy'].mean()

#%%
import chemparse

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

f_dicts = [chemparse.parse_formula(f) for f in df_prices_combine.index]
e_price = [calculate_formula_price(d) for d in f_dicts]
df_prices_combine['specific_price_element'] = e_price
df_prices_combine

#%%

#TODO: reexamine. Happening with Alva rock material (quartzite) that also doesn't happen to be on pubchem
# Need to figure out how to tie to USGS prices anyway
df_prices_combine = df_prices_combine.dropna(subset=['specific_price_refs', 'specific_price_element'], how='all')


#TODO: revisit. Was having issues with output changing with rounding errors
df_prices_combine['specific_price_refs'] = df_prices_combine['specific_price_refs'].apply(lambda x: round(x,7))
df_prices_combine['specific_price_element'] = df_prices_combine['specific_price_element'].apply(lambda x: round(x,7))

#%%


#TODO: Logic to get one price, didn't like averaging reference and elemntal price...but this isn't great eithger

specific_prices = []
price_types = []

for idx, row in df_prices_combine.iterrows():
    if row['specific_price_refs'] == row['specific_price_refs']:
        specific_price = row['specific_price_refs']
        price_type = 'Ref(s)' 
    else:
        specific_price = row['specific_price_element']
        price_type = 'Element'

    specific_prices.append(specific_price)
    price_types.append(price_type)

df_prices_combine['specific_price'] = specific_prices
df_prices_combine['price_type'] = price_types
    

    


#%%

df_prices_combine.to_csv('data/mat_prices.csv')



