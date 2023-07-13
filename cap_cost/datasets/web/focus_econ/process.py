
#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from es_utils.pdf import average_range
from es_utils.units import convert_units, prep_df_pint_out, ureg

if not os.path.exists('output'): os.mkdir('output')

df_mat = pd.read_csv('input_data/input_data.csv',index_col=0)

# df_SM =df_SM.drop([47,79,81,124]).reset_index(drop=True) # Seems to be a typo for cobalt entry

specific_price = df_mat['Q4 2022']


specific_price = specific_price.str.replace(',', '').astype('pint[USD/t]')

specific_price = specific_price.pint.to('USD/kg')

specific_price.name = 'specific_price'
specific_price.index.name = 'original_name'

specific_price

#%%

specific_price


from es_utils.chem import process_mat_lookup

mat_lookup = pd.read_csv('mat_lookup.csv')
mat_lookup = process_mat_lookup(mat_lookup)
df = pd.merge(specific_price, mat_lookup, on='original_name')


# df.to_csv('output/processed.csv', index=False)


from es_utils import extract_df_mat
df_price = extract_df_mat(df)

# df_price


# df_price = prep_df_pint_out(df_price)

# df_price.to_csv('output/mat_data.csv')

df = df.set_index('index')

df_combine = df.groupby('index')[['specific_price']].mean()

from es_utils import join_col_vals
df_combine['original_name']= df.groupby('index')['original_name'].apply(join_col_vals)
df_combine['molecular_formula']= df.groupby('index')['molecular_formula'].apply(join_col_vals)

from es_utils import extract_df_mat
df_price = extract_df_mat(df_combine)


df_price = convert_units(df_price)
df_price = prep_df_pint_out(df_price)

df_price.to_csv('output/mat_data.csv')
# %%
