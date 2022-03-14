import pandas as pd
import os
import es_utils

tables = {fn.strip('.csv') : pd.read_csv(os.path.join('tables',fn)) for fn in os.listdir('tables')}


df = pd.concat(tables.values())


df['specific_energy'] = df['specific_energy'].astype(float)
df['enthalpy'] = df['enthalpy'].astype(float)
df['temperature'] = df['temperature'].astype(float)

df['enthalpy'] = df['enthalpy']/3600 #kJ to kWh
df['specific_energy'] = df['specific_energy']/3600 #kJ to kWh

df = df.rename({
    'reactant':'original_name'
}, axis=1)

#If no lookup table is needed
# from es_utils.chem import mat2vec_process
# df['molecular_formula'] = df['original_name'].apply(mat2vec_process)

# index_use = 'molecular_formula'
# df['index_use'] = index_use
# df['index'] = df[index_use]
# df = df.set_index('index')

chem_lookup = pd.read_csv('chem_lookup.csv')
chem_lookup = es_utils.chem.process_chem_lookup(chem_lookup)
df = pd.merge(df, chem_lookup, on='original_name').set_index('index')

df.to_csv('output/process.csv')