#%%

import pandas as pd
import os

chem_lookup = pd.read_csv('output/chem_lookup.csv', index_col=0)
chem_lookup
# %%
table_3 = pd.read_csv('tables/table_3.csv', index_col=0)
table_3

#%%

present_chemicals = [name for name in table_3.index if name in chem_lookup.index]

table_3['chemical'] = chem_lookup.loc[present_chemicals]

# %%
table_3.to_csv('output/process.csv')
# %%
