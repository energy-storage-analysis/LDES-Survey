#%%
import pandas as pd
import os
import es_utils

tables = {fn.strip('.csv') : pd.read_csv(os.path.join('tables',fn)) for fn in os.listdir('tables')}

tables['table_1']['type'] = 'EDLC'
tables['table_2']['type'] = 'Pseudocapacitor'
tables['table_3']['type'] = 'Hybrid'


df = pd.concat(tables.values())

df = df.rename({
    'Materials': 'original_name',
    'Electrode System (1,2)': 'num_electrodes',
    'Specific Capacitance (F·g-1)': 'specific_capacitance',
    'Potential Range (V)': 'deltaV'
}, axis=1)

df = df.dropna(subset=['specific_capacitance'])

df = df.set_index('original_name')

# %%
from es_utils.pdf import average_range

df['specific_capacitance'] = df['specific_capacitance'].astype(str).apply(average_range)

#%%


if not os.path.exists('output'): os.mkdir('output')

df.to_csv('output/processed.csv')

# %%

chem_lookup = pd.read_csv('chem_lookup.csv')
chem_lookup = es_utils.chem.process_chem_lookup(chem_lookup, mtp=None)
df = pd.merge(df, chem_lookup, on='original_name').set_index('index')

from es_utils import extract_df_physprop
df_physprop = extract_df_physprop(df, ['specific_capacitance', 'deltaV', 'type']) #TODO: figure out how to combine with battery deltaV
#%%


df_physprop.to_csv('output/physprop.csv')
# %%
