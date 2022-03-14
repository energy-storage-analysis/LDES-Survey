#%%
import os
from os.path import join as pjoin
import numpy as np
import pandas as pd

dataset_folder = '../datasets'
dataset_index = pd.read_csv(pjoin(dataset_folder,'dataset_index.csv'), index_col=0)

col_select = ['material_name', 'molecular_formula', 'original_name','specific_price','specific_energy','source']
datasets = []

for source, row in dataset_index.iterrows():
    fp = os.path.join(dataset_folder, row['price_data_path'])
    df = pd.read_csv(fp,index_col=0)
    col_select_present = [col for col in col_select if col in df.columns]
    df = df[col_select_present]

    #Custom data dataset already has source column
    if source != 'custom_data':
        df['source'] = source

    datasets.append(df)

df = pd.concat(datasets)

df.index.name = 'index'

#%%
energy_type_lookup = {
    'Alva 2018 (Latent)': 'Latent Thermal',
    'Alva 2018 (Sensible)': 'Sensible Thermal',
    'Grosu 2017': 'Sensible Thermal', #TODO: this is only magnetite (called iron ore along iwth hematite). 
    'Ray 2021': 'Latent Thermal',
    'Andre 2016': 'Thermochemical',
    'Kale 2018': 'Virial'
}

energy_type = [energy_type_lookup[s] if s in energy_type_lookup else np.nan for s in df['source']]
df['energy_type'] = energy_type
#%%


## Collect prices 

#%%
def join_material_dups(df_dup, column):
    source_list = ", ".join(df_dup[column].dropna())
    return source_list


s_temp = df.groupby('index').apply(join_material_dups, column='source')
s_temp.name = 'source'
df_prices = s_temp.to_frame()

df_prices['material_names']= df.groupby('index').apply(join_material_dups, column='material_name')
df_prices['energy_types']= df.groupby('index').apply(join_material_dups, column='energy_type')
df_prices['num_source'] = df_prices['source'].str.split(',').apply(len)
df_prices['specific_price_refs'] = df.groupby('index')['specific_price'].mean()

# df_prices['specific_energy'] = df.groupby('index')['specific_energy'].mean()

df_prices

#%%


df_prices


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

f_dicts = [chemparse.parse_formula(f) for f in df_prices.index]
e_price = [calculate_formula_price(d) for d in f_dicts]
df_prices['specific_price_element'] = e_price
df_prices

#%%

#TODO: reexamine. Happening with Alva rock material (quartzite) that also doesn't happen to be on pubchem
# Need to figure out how to tie to USGS prices anyway
df_prices = df_prices.dropna(subset=['specific_price_refs', 'specific_price_element'], how='all')


#TODO: revisit. Was having issues with output changing with rounding errors
df_prices['specific_price_refs'] = df_prices['specific_price_refs'].apply(lambda x: round(x,7))
df_prices['specific_price_element'] = df_prices['specific_price_element'].apply(lambda x: round(x,7))

#%%

# df_prices['specific_price_avg'] = np.sum([
#     df_prices['specific_price_refs'],
#     df_prices['specific_price_element']
# ])/2


#TODO: Logic to get one price, didn't like averaging reference and elemntal price...but this isn't great eithger

specific_prices = []
price_types = []

for idx, row in df_prices.iterrows():
    if row['specific_price_refs'] == row['specific_price_refs']:
        specific_price = row['specific_price_refs']
        price_type = 'Ref(s)' 
    else:
        specific_price = row['specific_price_element']
        price_type = 'Element'

    specific_prices.append(specific_price)
    price_types.append(price_type)

df_prices['specific_price'] = specific_prices
df_prices['price_type'] = price_types
    

    


#%%

df_prices.to_csv('data/df_prices.csv')

#%%

# Apply prices to signle mat data
df['specific_price'] = [df_prices['specific_price'][f] if f in df_prices.index else np.nan for f in df.index]
df['price_type'] = [df_prices['price_type'][f] if f in df_prices.index else np.nan for f in df.index]



df.to_csv('data/df_singlemat.csv')



#%%


df_ec_li = pd.read_csv(r'C:\Users\aspit\Git\MHDLab-Projects\Energy Storage Analysis\datasets\pdf\li_2017\output\couples.csv',index_col=0)
df_ec_li['source'] = 'Li 2017'
df_ec_lmb = pd.read_csv(r'C:\Users\aspit\Git\MHDLab-Projects\Energy Storage Analysis\datasets\pdf\kim_2013\output\couples.csv', index_col=0)
df_ec_lmb['type'] = 'Liquid Metal'
df_ec_lmb['source'] = 'Kim 2013'

col_select = ['type','A','B','mu_A', 'mu_B', 'deltaV', 'specific_energy', 'source']

df_ec = pd.concat([
    df_ec_li[col_select],
    df_ec_lmb[col_select],
])

df_ec['SP_A'] = [df_prices['specific_price'][f] if f in df_prices.index else np.nan for f in df_ec['A']]
df_ec['SP_B'] = [df_prices['specific_price'][f] if f in df_prices.index else np.nan for f in df_ec['B']]

#TODO: chech this equation
df_ec['specific_price'] = (df_ec['SP_A']*df_ec['mu_A'] + df_ec['SP_B']*df_ec['mu_B'])/(df_ec['mu_A']+df_ec['mu_B'])

df_ec['energy_type'] = 'EC Couple'
df_ec.index.name = 'index'
df_ec['original_name'] = df_ec.index
df_ec['price_type'] = 'TODO'

df_ec.to_csv('data/df_couples.csv')
#%%



