#%%
import os
from os.path import join as pjoin
import numpy as np
import pandas as pd
from es_utils import join_col_vals
from es_utils.units import prep_df_pint_out, read_pint_df, ureg

from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

dataset_folder = 'datasets'
dataset_index = pd.read_csv(pjoin(dataset_folder,'dataset_index.csv'), index_col=0)
dataset_years = pd.read_csv(pjoin(dataset_folder,'dataset_years.csv'), index_col=0)['year'].dropna()

from es_utils.cpi import get_cpi_data
cpi_data = get_cpi_data()

#%%

# Consolidate together all data from folders listed in dataset_index.csv

dfs_mat_data = []
dfs_SM = []

for source, row in dataset_index.iterrows():
    fp_prices = os.path.join(dataset_folder, row['folder'], 'output', 'mat_data.csv')
    if os.path.exists(fp_prices):
        df_mat_data = read_pint_df(fp_prices)
        

        #Custom data dataset already has source column
        if 'source' not in df_mat_data.columns:
            df_mat_data['source'] = source

        if 'year' not in df_mat_data.columns:
            if source not in dataset_years.index:
                raise ValueError("Did not find a year for mat data source: {}".format(source))
            else:
                df_mat_data['year'] = dataset_years[source]

        dfs_mat_data.append(df_mat_data)


    fp_SM = os.path.join(dataset_folder, row['folder'], 'output', 'SM_data.csv')
    if os.path.exists(fp_SM):
        df_SM = read_pint_df(fp_SM)

        #Custom data dataset already has source column
        if 'source' not in df_SM.columns:
            df_SM['source'] = source

        dfs_SM.append(df_SM)

df_mat_data = pd.concat(dfs_mat_data)
df_SM = pd.concat(dfs_SM)
df_SM.index.name = 'SM_name'

#We are going to index by both SM_name and SM_type, then average all duplicate values that are floats
df_SM = df_SM.reset_index().set_index(['SM_name','SM_type'])

#%%

#Correct for inflation here
df_mat_data['specific_price'] = df_mat_data['specific_price']*df_mat_data['year'].map(cpi_data)

df_mat_data_all_out = prep_df_pint_out(df_mat_data)
df_mat_data_all_out.to_csv('data_consolidated/mat_data_all.csv')

# physical_property_lookup = pd.read_csv(os.path.join(REPO_DIR, 'cap_cost\data_consolidated\SM_column_info.csv'), index_col=0)['long_name']

df_SM_all_out = prep_df_pint_out(df_SM)
df_SM_all_out.to_csv('data_consolidated/SM_data_all.csv')


#%%

# Combine duplicate SM (SM_data_all) into one (SM_data)

# Combine float columns with method depending on physical propery, and Group together non-float columns into a string separated by commas
#TODO: Need to implement beter check here now that units are implemented. 
# If units are not setup properly in raw dataset then the dtype is an object and an error is thrown. 
# You can find which entries are floats (and not pint Quantity) with e.g. df_SM[df_SM['mass_density'].apply(type) == float]

# Remove some columns with extra information in the final dataset. 
df_SM = df_SM.drop(['kth', 'C_kwh_orig'], axis=1) # Drop columns that are unused in in the 

float_cols = []
for column in df_SM.columns:
    dtype = df_SM[column].dtype
    if dtype == float or 'pint' in str(dtype):
        float_cols.append(column)


other_cols = [c for c in df_SM.columns if c not in float_cols]

#%%

#Original method used when only averaging physical property values, can be used to check the same result when only using 'mean' as a duplicate col method
df_grouped = df_SM[float_cols].groupby(by=['SM_name','SM_type']).mean()

# #These are the columns that we have found to have multiple values from source (source_meta/physprop_info), and so we decide how to handle that for each physical property
duplicate_col_method = {
    'Cp': 'max',
    'T_melt': 'min',
    'T_max': 'max',
    'sp_latent_heat': 'max',
    'mass_density': 'mean', # For the duplicated values (sensible latent), this is not actually being used
    'phase_change_T': 'max'
}

# Uncomment to revert all to mean as previous method 
# duplicate_col_method = {key: 'mean' for key in duplicate_col_method}

def num_unique(l):
    return len(l.unique())

dfs = []

for col in float_cols:
    gb = df_SM[col].dropna().groupby(by=['SM_name','SM_type'])
    if col in duplicate_col_method:
        method = duplicate_col_method[col]
        if method=='max':
            df = gb.max()
        elif method=='min':
            df = gb.min()
        elif method=='mean':
            df = gb.mean()
        else:
            raise ValueError
    else:
        assert all(gb.apply(num_unique) == 1)
        df = df_SM[col].dropna()
        
    df = df.to_frame()
    dfs.append(df)

 
df_out = dfs[0].join(dfs[1:], how='outer').dropna(how='all')

#This methods adds a few duplicates and nan in the index for some reason. 
df_out = df_out[~df_out.index.duplicated()].dropna(how='all')
df_out = df_out.loc[df_out.index.dropna()]

df_out.equals(df_grouped) # Check that it gives the same value (see above)

df_grouped = df_out

#%%

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

# Determining T_min for Delta T calculations for sensible thermal . We first use
# melting temperature data or a default minimum tempratrue (room temperature),
# an pick whatever is highest for hot (or 'both') SM. For cold SM we use the
# melting temperature. For the remaining we use the default temperature.  

default_min_T = 20

df_melt = df_grouped.dropna(subset=['T_melt'])[['sub_type','mat_type']]

df_hot = df_melt.where(df_melt['sub_type'].isin(['hot','both'])).dropna(how='all')

def find_min_temp(T):
    T_min = T if T > default_min_T else default_min_T
    return T_min

df_grouped.loc[df_hot.index, 'T_min'] = df_grouped.loc[df_hot.index, 'T_melt'].pint.magnitude.apply(find_min_temp)

df_cold = df_melt.where(df_melt['sub_type'].isin(['cold'])).dropna(how='all')
df_grouped.loc[df_cold.index, 'T_min'] = df_grouped.loc[df_cold.index, 'T_melt'].pint.magnitude

# Remaining in the dataset without Tmin (but still with a Tmax)
remaining_sensible = df_grouped.dropna(subset=['T_max'])['T_min'].astype(float).fillna(default_min_T)
df_grouped.loc[remaining_sensible.index, 'T_min'] = remaining_sensible
df_grouped['T_min'] = df_grouped['T_min'].astype(float).astype('pint[degC]')

df_grouped['deltaT'] = df_grouped['T_max'] - df_grouped['T_min']
#%%

df_grouped_out = prep_df_pint_out(df_grouped)

df_grouped_out.to_csv('data_consolidated/SM_data.csv')


#%%

# Combine mat data into one. 

s_temp = df_mat_data.groupby('index')['source'].apply(join_col_vals, make_set=False, sort=False)
s_temp.name = 'sources'
df_prices_combine = s_temp.to_frame()

df_prices_combine['original_names'] = df_mat_data.groupby('index')['original_name'].apply(join_col_vals) 
df_prices_combine['num_source'] = df_prices_combine['sources'].str.split(',').apply(len)

# Need to transform into magnitude for min/max operation, so we ensure we are in the right units first
specific_price_mag = df_mat_data['specific_price'].pint.to('USD/kg').pint.magnitude
vol_price_mag = df_mat_data['vol_price'].pint.to('USD/m**3').pint.magnitude

# Pick method of combining prices here. 
df_prices_combine['specific_price'] = specific_price_mag.groupby('index').median()
df_prices_combine['vol_price'] = vol_price_mag.groupby('index').median()

df_prices_combine['specific_price'] = df_prices_combine['specific_price'].astype('pint[USD/kg]')
df_prices_combine['vol_price'] = df_prices_combine['vol_price'].astype('pint[USD/m**3]')

df_prices_combine['specific_prices'] = specific_price_mag.apply(lambda x: round(x,2)).astype(str).groupby('index').apply(join_col_vals, make_set=False, sort=False)

df_prices_combine['specific_price_std'] = df_mat_data.groupby('index')['specific_price'].std()
df_prices_combine['specific_price_std'] = df_prices_combine['specific_price_std'].astype(df_prices_combine['specific_price'].dtype)
df_prices_combine['specific_price_rat'] = df_prices_combine['specific_price_std']/df_prices_combine['specific_price'] 
df_prices_combine['specific_price_rat'] = df_prices_combine['specific_price_rat'].apply(lambda x:round(x,2)) 
df_prices_combine['specific_price_rat'] = df_prices_combine['specific_price_rat'].astype('pint[dimensionless]')


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

df_prices_combine = df_prices_combine[[
'specific_price', 'specific_price_std','specific_price_rat', 'vol_price','num_source','sources','specific_prices','molecular_formula','mu','original_names','specific_price_element',
]]


df_prices_combine = prep_df_pint_out(df_prices_combine)

df_prices_combine.to_csv('data_consolidated/mat_data.csv')
