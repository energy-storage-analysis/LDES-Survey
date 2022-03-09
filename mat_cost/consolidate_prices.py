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
df['molecular_formula_norm'] = df['molecular_formula'].astype(str).apply(mat2vec_process)
df['molecular_formula_norm'] = df['molecular_formula_norm'].replace('nan',np.nan) 
df



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

def join_material_dups(df_dup, column):
    source_list = ", ".join(df_dup[column].dropna())
    return source_list


s_mat_sources = df.groupby('material_name').apply(join_material_dups, column='source')
s_mat_sources.name = 'source'
df_material = s_mat_sources.to_frame()

existing_pubchem_form = [f for f in s_mat_sources.index if f in pubchem_forms.index] #TODO: must update pubchem_forms for new datasets...just need to redo indexing and pubchem

df_material['pubchem_formula'] = pubchem_forms.loc[existing_pubchem_form]
# df_material['specific_energy'] = df.groupby('material_name')['specific_energy'].mean() #specific energy for different forms of energy should not be combined, unlike price. 
df_material['specific_price'] = df.groupby('material_name')['specific_price'].mean()

df_material.to_csv('data/prices_material.csv')

# s_mat_sources.to_csv('material_sources.csv')

#%%


df_usgs_ise = df.where(df['source'].isin(['USGS', 'ISE'])).dropna(subset=['source','material_name'])


df_temp = df_usgs_ise.groupby('material_name')['specific_price'].mean().to_frame()
df_temp['sources'] = df.groupby('material_name').apply(join_material_dups, column='source') 

df_temp['pubchem_formula'] = pubchem_forms.loc[df_temp.index].values
df_temp = df_temp.drop_duplicates(subset=['pubchem_formula'])
df_temp = df_temp.reset_index().set_index('pubchem_formula')
df_temp




# df_matonly.set_index('material_name')
# df_matonly

# df_matonly.dropna(subset=['pubchem_formula'])
#%%

# form_process = [mat2vec_process(f) for f in df_molecular.index]
# df_molecular['formula_processed'] = form_process

s_molecular_sources = df.groupby('molecular_formula_norm').apply(join_material_dups, column='source')
s_molecular_sources.name = 'source'
df_molecular = s_molecular_sources.to_frame()

df_molecular['material_names_refs']= df.groupby('molecular_formula_norm').apply(join_material_dups, column='material_name')

# df_molecular['specific_energy'] = df.groupby('molecular_formula_norm')['specific_energy'].mean()
df_molecular['specific_price_refs'] = df.groupby('molecular_formula_norm')['specific_price'].mean()
# df_molecular = df_molecular.drop('nan')
#%%


present_chemicals = [c for c in df_molecular.index if c in df_temp.index]
df_molecular['specific_price_UI'] = df_temp.loc[present_chemicals]['specific_price']
df_molecular['material_name_UI'] = df_temp.loc[present_chemicals]['material_name']
df_molecular
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

f_dicts = [chemparse.parse_formula(f) for f in df_molecular.index]
e_price = [calculate_formula_price(d) for d in f_dicts]
df_molecular['specific_price_element'] = e_price
df_molecular

#%%
df_molecular.to_csv('data/prices_molecular.csv')

# s_molecular_sources.to_csv('molecular_sources.csv')

#%%
# for idx, row in df_material.iterrows():
#     f = row['pubchem_top_formula']
#     if f != 'nan':
#         if f in df['molecular_formula_norm'].dropna().values:
#             print("{} : {}".format(idx, f))
# %%
#%%

df_sp_energy = df.dropna(subset=['specific_energy', 'molecular_formula'])
df_sp_energy = df_sp_energy[['source','specific_energy', 'molecular_formula_norm']]
df_sp_energy


energy_type_lookup = {
    'Alva 2018 (Latent)': 'Latent Thermal',
    'Alva 2018 (Sensible)': 'Sensible Thermal',
    'Andre 2016': 'Thermochemical'
}

energy_type = [energy_type_lookup[s] for s in df_sp_energy['source']]
df_sp_energy['energy_type'] = energy_type

df_sp_energy.to_csv('data/sp_energy_molecular.csv')
# df_sp_energy = df_sp_energy[['molecular_formula_norm','specific_energy','source']]
# %%
