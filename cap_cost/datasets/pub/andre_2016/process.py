#%%
import pandas as pd
import os
import es_utils

tables = {fn.strip('.csv') : pd.read_csv(os.path.join('tables',fn)) for fn in os.listdir('tables')}

df = pd.concat(tables.values())

df[['reactant','product']] = df['original_name'].str.split('/', expand=True)

# df['enthalpy'] = df['enthalpy'].astype(float)
df = df.drop('enthalpy', axis=1) #TODO: the enthalpy data is molar, and pretty sure specific_energy just calculated using molar mass, but this should be done manually

df = df.rename({
    'specific_energy': 'deltaH_thermochem'
}, axis=1)

df['deltaH_thermochem'] = df['deltaH_thermochem'].astype(float)
df['deltaH_thermochem'] = df['deltaH_thermochem']/3600 #kJ to kWh

df['temperature'] = df['temperature'].astype(float)


chem_lookup = pd.read_csv('chem_lookup.csv')
chem_lookup = es_utils.chem.process_chem_lookup(chem_lookup)
df = pd.merge(df, chem_lookup, on='original_name').set_index('index')

SM_lookup = pd.read_csv('SM_lookup.csv', index_col=0)

df_SMs = df[['original_name','deltaH_thermochem','temperature','type']].set_index('original_name')

df_SMs = pd.merge(
    SM_lookup,
    df_SMs,
    on='original_name'
    
)


df_SMs.index.name = 'SM_name'
df_SMs.to_csv('output/SM_data.csv')
# %%
