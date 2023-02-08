#%%
from os.path import join as pjoin
import os
import pandas as pd

from es_utils.units import convert_units, prep_df_pint_out, ureg

if not os.path.exists('output'): os.mkdir('output')

#Table A1
df = pd.read_csv(pjoin('tables','table_S2.csv'))

df = df.rename({
    'MATERIAL': 'original_name',
    'DENSITY (g / cm3)': 'mass_density',
    'PRICE ($ / kg)': 'specific_price'
},axis=1)

df = df.drop('mass_density', axis=1) # Mass density is for storage media, not materials



mat_lookup = pd.read_csv('mat_lookup.csv', index_col=0)

from es_utils.chem import process_mat_lookup
mat_lookup = process_mat_lookup(mat_lookup)

df_mat = pd.merge(df, mat_lookup, on='original_name').set_index('index')

#%%

df_mat

#%%




from es_utils import extract_df_mat
from es_utils.units import read_pint_df
df_price = extract_df_mat(df_mat)

df_price = df_price.astype({
    'specific_price': 'pint[USD/kg]',
    })
#%%


df_price = convert_units(df_price)
df_price = prep_df_pint_out(df_price)


df_price.to_csv('output/mat_data.csv')

#%%