#%%
import pandas as pd
import os

if not os.path.exists('output'): os.mkdir('output')


tables = {fn.strip('.csv') : pd.read_csv(os.path.join('tables',fn), encoding='utf-8') for fn in os.listdir('tables')}

df = tables['table_2']

df = df.rename({
    'system': 'SM_name',
    'voltage': 'deltaV'
}, axis=1)

#TODO: Just keeping the first of the duplicate SM (i.e. with different products)
df = df.groupby('SM_name').first()

for col in ['specific_energy','energy_density','deltaV']:
    df[col] = df[col].str.replace('~', '', regex=False).astype(float)

#TODO: carry over orignal specific energy calculation? At least compare
df = df[['deltaV']]

SM_lookup = pd.read_csv('SM_lookup.csv', index_col=0)

df = pd.merge(df, SM_lookup, on='SM_name')

df['SM_type'] ='metal_air'

df.to_csv('output/SM_data.csv')