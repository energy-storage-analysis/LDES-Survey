#%%
import os
from os.path import join as pjoin
import numpy as np
import pandas as pd
from es_utils import join_col_vals

dataset_folder = '../datasets'
dataset_index = pd.read_csv(pjoin(dataset_folder,'dataset_index.csv'), index_col=0)

# col_select = ['material_name', 'molecular_formula', 'original_name','specific_price','specific_energy','energy_type','source']
dfs_mat_data = []
dfs_SM = []

for source, row in dataset_index.iterrows():
    fp_prices = os.path.join(dataset_folder, row['folder'], 'output', 'mat_data.csv')
    if os.path.exists(fp_prices):
        df_mat_data = pd.read_csv(fp_prices,index_col=0)

        #Custom data dataset already has source column
        if source != 'custom_data':
            df_mat_data['source'] = source

        dfs_mat_data.append(df_mat_data)


    fp_SM = os.path.join(dataset_folder, row['folder'], 'output', 'SM_data.csv')
    if os.path.exists(fp_SM):
        df_SM = pd.read_csv(fp_SM,index_col=0)

        #Custom data dataset already has source column
        if source != 'custom_data':
            df_SM['source'] = source

        dfs_SM.append(df_SM)

df_mat_data = pd.concat(dfs_mat_data)
df_SM = pd.concat(dfs_SM)
df_SM.index.name = 'SM_name'

# df_SM = df_SM[]

# df.index.name = 'index'

#%%

# SM_cols = ['energy_type','materials','source','C_kwh_orig','type','deltaV','original_name','delta_height','specific_capacitance']

# df_SM = df_SM[SM_cols]


df_SM.to_csv('data/SMs.csv')


#%%
df_mat_data.to_csv('data/mat_data_all.csv')

## Collect prices 

#%%

from es_utils import join_col_vals

s_temp = df_mat_data.groupby('index').apply(join_col_vals, column='source')
s_temp.name = 'source'
df_prices_combine = s_temp.to_frame()

df_prices_combine['num_source'] = df_prices_combine['source'].str.split(',').apply(len)
df_prices_combine['specific_price_refs'] = df_mat_data.groupby('index')['specific_price'].mean()



# df_prices['specific_energy'] = df.groupby('index')['specific_energy'].mean()

#%%
import chemparse

element_prices = pd.read_csv(
    os.path.join(dataset_folder, r'wiki_element_cost\output\process.csv')
    , index_col=1)


from es_utils.chem import calculate_formula_price

f_dicts = [chemparse.parse_formula(f) for f in df_prices_combine.index]
e_price = [calculate_formula_price(d, element_prices) for d in f_dicts]
df_prices_combine['specific_price_element'] = e_price
df_prices_combine

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
    
#TODO: revisit. Was having issues with output changing with rounding errors
df_prices_combine['specific_price_refs'] = df_prices_combine['specific_price_refs'].apply(lambda x: round(x,7))

#%%
#Should only be one molecular formula
df_prices_combine['molecular_formula'] = df_mat_data.groupby('index').apply(join_col_vals, column='molecular_formula')

from es_utils.chem import get_molecular_mass
df_prices_combine['mu'] = df_prices_combine['molecular_formula'].apply(get_molecular_mass)
    


#%%

df_prices_combine.to_csv('data/mat_data.csv')



#%%


# s_temp = df_mat_data.groupby('index').apply(join_col_vals, column='source')
# s_temp.name = 'source'
# df_physprop_combine = s_temp.to_frame()

# df_physprop_combine['num_source'] = df_physprop_combine['source'].str.split(',').apply(len)


# physprop_cols = ['Cp','kth','sp_latent_heat','phase_change_T','deltaH_thermochem','specific_strength', 'deltaG_chem','mass_density','dielectric_breakdown','dielectric_constant']

# for col in physprop_cols:
#     df_physprop_combine[col] = df_mat_data.groupby('index')[col].mean()

# df_physprop_combine.to_csv('data/mat_physprop.csv')