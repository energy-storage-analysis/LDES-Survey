
#%%
import pandas as pd
import os

from sympy import O



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
chem_lookup = pd.read_csv('chem_lookup.csv', index_col=0)

chem_lookup['pubchem_cid'] = chem_lookup['pubchem_cid'].astype(pd.Int64Dtype())
# present_chemicals = df['original_name'].values


df_out = pd.merge(df,chem_lookup,on='original_name')


#%%

import pubchempy as pcp

df_out['molecular_formula'] = df_out['pubchem_cid'].dropna().apply(lambda x: pcp.Compound.from_cid(x).molecular_formula)


#%%



df_out.loc['Vermiculite','molecular_formula'] = df_out.loc['Vermiculite','molecular_formula'].replace('-3','')


#%%

if not os.path.exists('output'): os.mkdir('output')

df_out.to_csv('output/processed.csv')
# %%
