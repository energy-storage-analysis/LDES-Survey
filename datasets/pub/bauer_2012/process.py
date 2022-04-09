#%%
import pandas as pd
import os

if not os.path.exists('output'): os.mkdir('output')
tables = {fn.strip('.csv') : pd.read_csv(os.path.join('tables',fn), encoding='utf-8', index_col=0) for fn in os.listdir('tables')}

df_t3 = tables['table_3']

df_t3 = df_t3.rename({
    'T  (◦C)': 'T', 
    'ρ  (kg·m−3)': 'mass_density', 
    'cp  (kJ·kg−1·K−1)': 'Cp', 
    'λ  (W·m−1·K−1)': 'kth',
    '106×a  (m2·s−1)': 'a', 
    '10−3×b  (J·m−2·K−1·s−1/2)': 'b'
}, axis=1)

df_t3.index.name = 'original_name'

df_t3 = df_t3[['mass_density','Cp','kth']]

SM_lookup = pd.read_csv('SM_lookup.csv')
df = pd.merge(df_t3, SM_lookup, on='original_name')

df = df.dropna(subset=['SM_name'])

df = df.set_index('SM_name')

df['Cp'] = df['Cp']/3600

df
# %%

df.to_csv('output/SM_data.csv')
# %%
