#%%
import os
from os.path import join as pjoin
import numpy as np
import pandas as pd
from mat2vec.processing import MaterialsTextProcessor
mtp = MaterialsTextProcessor()

def mat2vec_process(f):
    return mtp.process(f)[0][0]

dataset_folder = '../datasets'
dataset_index = pd.read_csv(pjoin(dataset_folder,'dataset_index.csv'), index_col=0)

col_select = ['material_name', 'molecular_formula', 'specific_price','specific_energy']
datasets = []

for source, row in dataset_index.iterrows():
    fp = os.path.join(dataset_folder, row['path'])
    df = pd.read_csv(fp)
    col_select_present = [col for col in col_select if col in df.columns]
    df = df[col_select_present]

    if source == 'USGS':
        df_1 = df.groupby('material_name')['specific_price'].mean()
        df_1 = df_1.to_frame().reset_index()
        df_2 = df.groupby('molecular_formula')['specific_price'].mean()
        df_2 = df_2.to_frame().reset_index()
        
        df = pd.concat([df_1, df_2]).reset_index(drop=True)

    if source == 'ISE':
        sp_price_mean = df.groupby('material_name')['specific_price'].mean()
        df = sp_price_mean.to_frame().reset_index()
        # test

    df['source'] = source

    datasets.append(df)

df = pd.concat(datasets).reset_index(drop=True)

df['material_name'] = df['material_name'].str.lower()
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

pubchem_lookup = pd.read_csv(r'data\pubchem_lookup.csv', index_col=0)

#TODO: lowercase original pubchem lookup
pubchem_lookup = pubchem_lookup.reset_index()
pubchem_lookup['index'] = pubchem_lookup['index'].str.lower()
pubchem_lookup = pubchem_lookup.drop_duplicates(subset=['index'])
pubchem_lookup = pubchem_lookup.set_index('index')

pubchem_lookup

#%%

pubchem_forms = pubchem_lookup['pubchem_top_formula'].astype(str).apply(mat2vec_process)
pubchem_forms = pubchem_forms.replace('nan', np.nan)
pubchem_forms

#%%

pubchem_forms.where(pubchem_forms.duplicated(False)).dropna()

#%%
#TODO: implement index_name upstream, so the name of materials can be set explicity by source. 

#For data where formula is missing, we are going to use pubchem index

df_temp = df.where(df['molecular_formula'].isna()).dropna(subset=['material_name'])

formulas = [pubchem_forms[m] if m in pubchem_forms.index else np.nan for m in df_temp['material_name'] ]


df_temp['molecular_formula'] = formulas

df.loc[df_temp.index, 'molecular_formula'] = df_temp['molecular_formula']
df
#%%


df['molecular_formula_norm'] = df['molecular_formula'].astype(str).apply(mat2vec_process)
df['molecular_formula_norm'] = df['molecular_formula_norm'].replace('nan',np.nan) 
df

#%%

# If the formula is missing, then use the material name for the index_name

df['index_name'] = df['molecular_formula_norm'].where(~df['molecular_formula_norm'].isna(), df['material_name'])
df = df.dropna(subset=['index_name'])

df.to_csv('data/combined_all.csv')
#%%
def join_material_dups(df_dup, column):
    source_list = ", ".join(df_dup[column].dropna())
    return source_list


s_temp = df.groupby('index_name').apply(join_material_dups, column='source')
s_temp.name = 'source'
df_price = s_temp.to_frame()

df_price['material_names']= df.groupby('index_name').apply(join_material_dups, column='material_name')
df_price['energy_types']= df.groupby('index_name').apply(join_material_dups, column='energy_type')
df_price['num_source'] = df_price['source'].str.split(',').apply(len)
df_price['specific_price_refs'] = df.groupby('index_name')['specific_price'].mean()

# df_price['specific_energy'] = df.groupby('index_name')['specific_energy'].mean()

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

df_price.to_csv('data/df_prices.csv')


#%%

