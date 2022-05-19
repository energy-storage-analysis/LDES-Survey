
#%%
import pandas as pd
import os
from es_utils.units import convert_units, prep_df_pint_out, ureg

if not os.path.exists('output'): os.mkdir('output')

df = pd.read_csv('tables/table_4.csv', index_col=0)

df = df.rename({
    'Cost/kg ($US/kg)': 'specific_price',
    'name': 'original_name',
    'Material': 'material_type'
}, axis=1)

df = df.astype({
    'specific_price': 'pint[USD/kg]',
    })


df = df.set_index('original_name', drop=True)
df['material_type'] = df['material_type'].ffill()

#%%
from es_utils.chem import process_chem_lookup

chem_lookup = pd.read_csv('chem_lookup.csv')
chem_lookup = process_chem_lookup(chem_lookup)
df = pd.merge(df, chem_lookup, on='original_name').set_index('index')
#%%
df

from es_utils import extract_df_mat
df_price = extract_df_mat(df)


df_price = convert_units(df_price)
df_price = prep_df_pint_out(df_price)
df_price.to_csv('output/mat_data.csv')

