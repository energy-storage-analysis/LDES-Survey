#%%
import os
from os.path import join as pjoin
import numpy as np
import pandas as pd
from es_utils.chem import mat2vec_process

dataset_folder = '../datasets'
dataset_index = pd.read_csv(pjoin(dataset_folder,'dataset_index.csv'), index_col=0)

col_select = ['material_name', 'molecular_formula', 'specific_price','specific_energy']
datasets = []

for source, row in dataset_index.iterrows():
    fp = os.path.join(dataset_folder, row['price_data_path'])
    df = pd.read_csv(fp,index_col=0)
    col_select_present = [col for col in col_select if col in df.columns]
    df = df[col_select_present]

    if source in ['USGS','ISE']:
        sp_price_mean = df.groupby('index')['specific_price'].mean()
        df = sp_price_mean.to_frame()
        break

    df['source'] = source

    datasets.append(df)

df = pd.concat(datasets)

df.index.name = 'index'

#%%
energy_type_lookup = {
    'Alva 2018 (Latent)': 'Latent Thermal',
    'Alva 2018 (Sensible)': 'Sensible Thermal',
    'Andre 2016': 'Thermochemical',
    'Kale 2018': 'Virial'
}

energy_type = [energy_type_lookup[s] if s in energy_type_lookup else np.nan for s in df['source']]
df['energy_type'] = energy_type
#%%


df.to_csv('data/df_singlemat.csv')


## Collect prices 

#%%
def join_material_dups(df_dup, column):
    source_list = ", ".join(df_dup[column].dropna())
    return source_list


s_temp = df.groupby('index').apply(join_material_dups, column='source')
s_temp.name = 'source'
df_price = s_temp.to_frame()

df_price['material_names']= df.groupby('index').apply(join_material_dups, column='material_name')
df_price['energy_types']= df.groupby('index').apply(join_material_dups, column='energy_type')
df_price['num_source'] = df_price['source'].str.split(',').apply(len)
df_price['specific_price_refs'] = df.groupby('index')['specific_price'].mean()

# df_price['specific_energy'] = df.groupby('index')['specific_energy'].mean()

df_price

#%%


df_price


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

f_dicts = [chemparse.parse_formula(f) for f in df_price.index]
e_price = [calculate_formula_price(d) for d in f_dicts]
df_price['specific_price_element'] = e_price
df_price

#%%

#TODO: reexamine. Happening with Alva rock material (quartzite) that also doesn't happen to be on pubchem
# Need to figure out how to tie to USGS prices anyway
df_price = df_price.dropna(subset=['specific_price_refs', 'specific_price_element'], how='all')


#%%

df_price['specific_price_avg'] = sum([
    df_price['specific_price_refs'].fillna(0),
    df_price['specific_price_element'].fillna(0)
])/2


#%%

df_price.to_csv('data/df_prices.csv')


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

df_ec.to_csv('data/df_couples.csv')
#%%



