#%%

import pandas as pd
import numpy as np
import os

chem_lookup = pd.read_csv('output/chem_lookup.csv', index_col=0)
chem_lookup
# %%
table_3 = pd.read_csv('tables/table_3.csv', index_col=0)
table_3

#%%

present_chemicals = [name for name in table_3.index if name in chem_lookup.index]

table_3['molecular_formula'] = chem_lookup.loc[present_chemicals]['molecular_formula']
table_3['material_name'] = chem_lookup.loc[present_chemicals]['material_name']

added_rows = pd.DataFrame({
    'molecular_formula': ['O2'],
    'ref': [np.nan],
    'specific_price': [0]
}, index = ['Air'])

table_3 = table_3.append(added_rows)

table_3

# %%
table_3.to_csv('output/process.csv')
# %%
