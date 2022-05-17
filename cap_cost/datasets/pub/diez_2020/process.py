#%%
import pandas as pd
import os

if not os.path.exists('output'): os.mkdir('output')
tables = {fn.strip('.csv') : pd.read_csv(os.path.join('tables',fn), encoding='utf-8', index_col=0) for fn in os.listdir('tables')}
#%%

df_t1 = tables['table_1']
df_t1.columns
#%%

df_t1 = df_t1.rename({
'E0 (V)': 'deltaV', 
'Energy densitya\r\n(Wh L−1)': 'vol_energy_density', 
'Cost (€ kW−1 h−1)d\t': 'C_kwh_orig', 
}, axis=1)

df_t1.index.name = 'original_name'

df_t1 = df_t1[['deltaV','C_kwh_orig']]


#%%
df_t2 = tables['table_2']
df_t2.columns
#%%

df_t2 = df_t2.rename({
'E0 (V)': 'deltaV', 
'Cost ($ kW?1 h?1)b': 'C_kwh_orig', 
}, axis=1)

df_t2.index.name = 'original_name'

df_t2 = df_t2[['deltaV','C_kwh_orig']]

df_t2

#%%

df = pd.concat([
    df_t1,
    df_t2
])


df['C_kwh_orig'] = df['C_kwh_orig'].str.replace('<', '')
df['C_kwh_orig'] = df['C_kwh_orig'].str.replace('-', '')
df['C_kwh_orig'] = df['C_kwh_orig'].str.replace('N. A.', '', regex=False)

SM_lookup = pd.read_csv('SM_lookup.csv')
df = pd.merge(df, SM_lookup, on='original_name')
df = df.dropna(subset=['SM_name'])
df = df.set_index('SM_name')

df = df.dropna(subset=['materials'])

#%%
#Data not included in tables
custom_data = pd.read_csv('tables/custom.csv', index_col=0)

df = pd.concat([df, custom_data])

# %%

df.to_csv('output/SM_data.csv')