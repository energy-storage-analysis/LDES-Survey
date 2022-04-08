#%%
import pandas as pd
import os

if not os.path.exists('output'): os.mkdir('output')
tables = {fn.strip('.csv') : pd.read_csv(os.path.join('tables',fn), encoding='utf-8', index_col=0) for fn in os.listdir('tables')}


# SM_lookup = pd.read_csv('SM_lookup.csv', index_col=0)
# df = pd.merge(df, SM_lookup, on='SM_name')

# %%
# df.to_csv('output/SM_data.csv')