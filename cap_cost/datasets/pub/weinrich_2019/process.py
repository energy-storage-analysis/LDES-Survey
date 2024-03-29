#%%
import pandas as pd
import os
from es_utils.units import convert_units, prep_df_pint_out, ureg

if not os.path.exists('output'): os.mkdir('output')


tables = {fn.strip('.csv') : pd.read_csv(os.path.join('tables',fn), encoding='utf-8') for fn in os.listdir('tables')}

df = tables['table_1']

df = df.rename({
    'system': 'original_name',
    'voltage': 'deltaV'
}, axis=1)

#TODO: Just keeping the first of the duplicate SM (i.e. with different products)
df = df.groupby('original_name').first()

df['n_e'] = df['n_e'].str.replace('[\*†\n]','', regex=True).astype(int)

#%%

for col in ['deltaV']:
    df[col] = df[col].str.replace('~', '', regex=False).astype(float)

#TODO: carry over orignal specific energy calculation? At least compare
df = df[['deltaV', 'n_e']]

SM_lookup = pd.read_csv('SM_lookup.csv', index_col=0)

df = pd.merge(df, SM_lookup, on='original_name')
df = df.reset_index().set_index('SM_name')


df = df.astype({
    'deltaV': 'pint[V]',
    'n_e': 'pint[dimensionless]',
    })

df = convert_units(df)
df = prep_df_pint_out(df)

df.to_csv('output/SM_data.csv')