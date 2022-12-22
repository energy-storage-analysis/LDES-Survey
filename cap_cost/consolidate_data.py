#%%
import os
from os.path import join as pjoin
import numpy as np
import pandas as pd
from es_utils import join_col_vals
from es_utils.units import prep_df_pint_out, read_pint_df, ureg

dataset_folder = 'datasets'
dataset_index = pd.read_csv(pjoin(dataset_folder,'dataset_index.csv'), index_col=0)

# col_select = ['material_name', 'molecular_formula', 'original_name','specific_price','specific_energy','energy_type','source']
dfs_mat_data = []
dfs_SM = []

for source, row in dataset_index.iterrows():
    fp_prices = os.path.join(dataset_folder, row['folder'], 'output', 'mat_data.csv')
    if os.path.exists(fp_prices):
        # df_mat_data = pd.read_csv(fp_prices, header = [0,1], index_col=0)
        df_mat_data = read_pint_df(fp_prices)
        

        #Custom data dataset already has source column
        if 'source' not in df_mat_data.columns:
            df_mat_data['source'] = source

        dfs_mat_data.append(df_mat_data)


    fp_SM = os.path.join(dataset_folder, row['folder'], 'output', 'SM_data.csv')
    if os.path.exists(fp_SM):
        # df_SM = pd.read_csv(fp_SM,index_col=0)
        df_SM = read_pint_df(fp_SM)

        #Custom data dataset already has source column
        if 'source' not in df_SM.columns:
            df_SM['source'] = source

        dfs_SM.append(df_SM)

df_mat_data = pd.concat(dfs_mat_data)
df_SM = pd.concat(dfs_SM)
df_SM.index.name = 'SM_name'

# df_SM = df_SM[]

# df.index.name = 'index'

#%%

#We are going to index by both SM_name and SM_type, then average all duplicate values that are floats

df_SM = df_SM.reset_index().set_index(['SM_name','SM_type'])

#%%

# Average float columns and Group together non-float columns
#TODO: Need to implement beter check here now that units are implemented. 
# If units are not setup properly in raw dataset then the dtype is an object and an error is thrown. 
# You can find which entries are floats (and not pint Quantity) with e.g. df_SM[df_SM['mass_density'].apply(type) == float]

float_cols = []
for column in df_SM.columns:
    dtype = df_SM[column].dtype
    if dtype == float or 'pint' in str(dtype):
        float_cols.append(column)


other_cols = [c for c in df_SM.columns if c not in float_cols]

df_grouped = df_SM[float_cols].groupby(level=[0,1]).mean()


#List of columns that must have a single value, meaning an error is thrown if different sources have different values
#TODO: this needs to be applied to the SM_type in the index as well. 
single_value_cols = ['sub_type','mat_type', 'materials']

#TODO: the join col vals function should be able to work over multiple columns
for column in other_cols:
    if column in single_value_cols:

        #For columns that should be single-valued we check that the length of a set of the values is one. 
        #TODO: an alternative approach would be to have a second lookup table mapping storage medium index to these values, but keeping all lookup happening in individual sources for now.
        df_grouped[column] = df_SM[other_cols].groupby(level=[0,1])[column].apply(set)
        n_vals = df_grouped[column].apply(len)
        
        multiple_vals = n_vals[n_vals > 1].dropna()
        if len(multiple_vals):
            val_info = df_SM[['source',column]].loc[multiple_vals.index]
            raise ValueError("Got multiple values for single-valued column: {}\n\nprinting data: {}".format(column, val_info))

        # Finally if there are no errors then take first item of the set, which should be the only one
        df_grouped[column] = df_grouped[column].apply(lambda x: list(x)[0])
            
    else:
        df_grouped[column] = df_SM[other_cols].groupby(level=[0,1])[column].apply(join_col_vals)


#TODO: rename others to indicate multiple sources
# the other columns probably don't have duplciates, would be nice to have some quick way to know if there are duplicate values at all
df_grouped = df_grouped.rename({'source': 'SM_sources'}, axis=1)


#%%

#Doing this here to be able to see deltaT in SM_data

default_min_T = 20

df_grouped['T_min'] = df_grouped['T_melt'].fillna(default_min_T)
df_grouped['deltaT'] = df_grouped['T_max'] - df_grouped['T_min']
#%%

df_grouped_out = prep_df_pint_out(df_grouped)

df_grouped_out.to_csv('data_consolidated/SM_data.csv')


#%%

df_mat_data_all_out = prep_df_pint_out(df_mat_data)

df_mat_data_all_out.to_csv('data_consolidated/mat_data_all.csv')

## Collect prices 

#%%


s_temp = df_mat_data.groupby('index')['source'].apply(join_col_vals)
s_temp.name = 'sources'
df_prices_combine = s_temp.to_frame()

df_prices_combine['original_names'] = df_mat_data.groupby('index')['original_name'].apply(join_col_vals) 
df_prices_combine['num_source'] = df_prices_combine['sources'].str.split(',').apply(len)

specific_price_mag = df_mat_data['specific_price'].pint.magnitude
df_prices_combine['specific_price'] = df_mat_data.groupby('index')['specific_price'].median()

df_prices_combine['specific_prices'] = specific_price_mag.apply(lambda x: round(x,2)).astype(str).groupby('index').apply(join_col_vals)

df_prices_combine['specific_price_std'] = df_mat_data.groupby('index')['specific_price'].std()
df_prices_combine['specific_price_std'] = df_prices_combine['specific_price_std'].astype(df_prices_combine['specific_price'].dtype)
df_prices_combine['specific_price_rat'] = df_prices_combine['specific_price_std']/df_prices_combine['specific_price'] 
df_prices_combine['specific_price_rat'] = df_prices_combine['specific_price_rat'].apply(lambda x:round(x,2)) 
df_prices_combine['specific_price_rat'] = df_prices_combine['specific_price_rat'].astype('pint[dimensionless]')

vol_price_mag = df_mat_data['vol_price'].pint.magnitude
df_prices_combine['vol_price'] = df_mat_data.groupby('index')['vol_price'].median()
# df_prices['specific_energy'] = df.groupby('index')['specific_energy'].mean()

#%%
import chemparse

element_prices = pd.read_csv(
    os.path.join(dataset_folder, r'unused\wiki_element_cost\output\process.csv')
    , index_col=1)


from es_utils.chem import calculate_formula_price

f_dicts = [chemparse.parse_formula(f) for f in df_prices_combine.index]
e_price = [calculate_formula_price(d, element_prices) for d in f_dicts]
df_prices_combine['specific_price_element'] = e_price
df_prices_combine['specific_price_element'] = df_prices_combine['specific_price_element'].apply(lambda x: round(x,7))
df_prices_combine


#%%
#Should only be one molecular formula
df_prices_combine['molecular_formula'] = df_mat_data.groupby('index')['molecular_formula'].apply(join_col_vals)

from es_utils.chem import get_molecular_mass
df_prices_combine['mu'] = df_prices_combine['molecular_formula'].apply(get_molecular_mass)
df_prices_combine['mu'] = df_prices_combine['mu'].apply(lambda x: round(x,7))

df_prices_combine['mu'] = df_prices_combine['mu'].astype('pint[g/mol]')

#%%

import ast
mats = df_grouped['materials']

mats_single = mats.where(~mats.str.contains('[', regex=False)).dropna()
mats_comp = mats.where(mats.str.contains('[', regex=False)).dropna()
mats_comp = mats_comp.apply(ast.literal_eval)



num_sms = []
for idx in df_prices_combine.index:
    n = 0 
    for mat_name in mats_single.values:
        if mat_name == idx:
            n = n+1
    for comp_list in mats_comp:
        mats = [t[0] for t in comp_list]
        if idx in mats:
            n = n+1

    num_sms.append(n)

df_prices_combine['num_SMs'] = num_sms

#%%


df_prices_combine = df_prices_combine[[
'specific_price', 'specific_price_std','specific_price_rat', 'vol_price','num_SMs','num_source','sources','specific_prices','molecular_formula','mu','original_names','specific_price_element',
]]


df_prices_combine = prep_df_pint_out(df_prices_combine)

df_prices_combine.to_csv('data_consolidated/mat_data.csv')



#%%


# s_temp = df_mat_data.groupby('index')['source'].apply(join_col_vals)
# s_temp.name = 'source'
# df_physprop_combine = s_temp.to_frame()

# df_physprop_combine['num_source'] = df_physprop_combine['source'].str.split(',').apply(len)


# physprop_cols = ['Cp','kth','sp_latent_heat','phase_change_T','deltaH_thermochem','specific_strength', 'deltaG_chem','mass_density','dielectric_breakdown','dielectric_constant']

# for col in physprop_cols:
#     df_physprop_combine[col] = df_mat_data.groupby('index')[col].mean()

# df_physprop_combine.to_csv('data_consolidated/mat_physprop.csv')