#%%
import pandas as pd
import os

if not os.path.exists('output'): os.mkdir('output')
tables = {fn.strip('.csv') : pd.read_csv(os.path.join('tables',fn), encoding='utf-8', index_col=0) for fn in os.listdir('tables')}
#%%

df = tables['table_1']
df.columns
#%%

df = df.rename({

}, axis=1)

df

# df.to_csv('SM_lookup.csv')
#%%

# df = df.rename({}, axis=1)

# SM_lookup = pd.read_csv('SM_lookup.csv')
# df = pd.merge(df_t3, SM_lookup, on='original_name')
# df = df.dropna(subset=['SM_name'])
# df = df.set_index('SM_name')


# %%

# df.to_csv('output/SM_data.csv')