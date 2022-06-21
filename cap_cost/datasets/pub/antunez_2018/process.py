#%%
import pandas as pd
import os
import numpy as np
from sympy import O
from es_utils.units import prep_df_pint_out, convert_units
import es_utils

if not os.path.exists('output'): os.mkdir('output')
tables = {fn.strip('.csv') : pd.read_csv(os.path.join('tables',fn), encoding='utf-8', index_col=0) for fn in os.listdir('tables')}
#%%

# Output the columns of a table into the Ipython console and copy to the rename dictonary below to rename the columns. 

df = tables['table_1']
df.columns
#%%

df = df.rename({
' Tmin ◦C (K) ': 'T_melt', 
' Tmax ◦C (K) ': 'T_max', 
' cp  kJ/kg K': 'Cp', 
' ρ t/m3 ': 'mass_density',
'k   W/m K': 'kth', 
' µ  mPa s': 'viscosity', 
'cp,max  cp,min ': 'cp_max cp_min', 
'Ref.   ': 'ref',
'Exergy  Wh/kg (kWh/m3- ': 'specific_exergy', 
'Cost   USD/kg': 'specific_price', 
'Cost/exergy   USD/kWh': 'C_kwh_orig'
}, axis=1)


#TODO: add some of these back in, particularly mass density
df = df.drop(['ref', 'cp_max cp_min','viscosity','specific_exergy', 'mass_density'], axis=1)

df

# df.to_csv('SM_lookup.csv')
#%%

#TODO: improve naming of temperature and handling of cold store? Technichally these are still right...

df['T_melt'] = df['T_melt'].str.replace(' \(.+', '', regex=True)
df['T_max'] = df['T_max'].str.replace(' \(.+', '', regex=True)
# df['specific_exergy'] = df['specific_exergy'].str.replace(' \(.+', '')


#%%
for col in df.columns:
    df[col] = df[col].replace('-',np.nan).astype(float)


#%%

# Create these files, delete columns other than original_name, then add lookup columns as describd in readme

df.index.name = 'original_name'

# df.to_csv('SM_lookup.csv')
# df.to_csv('mat_lookup.csv')

#%%

unit_row = ['degC','degC', 'kJ/kg/K','W/m/K','USD/kg','USD/kWh']
df.columns = [df.columns, unit_row]

df = df.pint.quantify(level=-1)



#%%

SM_lookup = pd.read_csv('SM_lookup.csv')

df_SM = df.drop('specific_price', axis=1)

df_SM = pd.merge(df_SM, SM_lookup, on='original_name')
df_SM = df_SM.dropna(subset=['SM_name'])
df_SM = df_SM.set_index('SM_name')


df_SM = convert_units(df_SM)
df_SM = prep_df_pint_out(df_SM)

df_SM.to_csv('output/SM_data.csv')
# %%

df.index.name = 'original_name'

mat_lookup = pd.read_csv('mat_lookup.csv')
mat_lookup = es_utils.chem.process_chem_lookup(mat_lookup)


df_mat = df[['specific_price']]

df_mat = pd.merge(df_mat, mat_lookup, on='original_name')
df_mat = df_mat.dropna(subset=['index'])
df_mat = df_mat.set_index('index')

df_mat = convert_units(df_mat)
df_mat = prep_df_pint_out(df_mat)


df_mat.to_csv('output/mat_data.csv')
# %%
