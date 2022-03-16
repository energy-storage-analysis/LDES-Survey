
#%%
import pandas as pd
import os


df = pd.read_csv('tables/table_4.csv', index_col=0)

df = df.rename({
    'Cost/kg ($US/kg)': 'specific_price',
    'name': 'original_name',
    'Material': 'material_type'
}, axis=1)


df = df.set_index('original_name', drop=True)
df['material_type'] = df['material_type'].ffill()



df
#%%
from es_utils.chem import process_chem_lookup

chem_lookup = pd.read_csv('chem_lookup.csv')
chem_lookup = process_chem_lookup(chem_lookup)
df = pd.merge(df, chem_lookup, on='original_name').set_index('index')
#%%
df


#%%

# import pubchempy as pcp

# df_out['molecular_formula'] = df_out['pubchem_cid'].dropna().apply(lambda x: pcp.Compound.from_cid(x).molecular_formula)

#%%

if not os.path.exists('output'): os.mkdir('output')

df.to_csv('output/processed.csv')
# %%
