"""
Processing script template. This template is designed to work on extracted data (e.g. tables from pdf obtained from extract_template.py)
"""

#%%
import pandas as pd
import numpy as np
import os
from es_utils.units import prep_df_pint_out, convert_units
from es_utils.chem import process_chem_lookup
from es_utils.pdf import average_range

if not os.path.exists('output'): os.mkdir('output')
tables = {fn.strip('.csv') : pd.read_csv(os.path.join('tables',fn), encoding='utf-8', index_col=0) for fn in os.listdir('tables')}
#%%

# Output the columns of a table into the Ipython console and copy to the rename dictonary below to rename the columns. 

df = tables['table_A2']
df.columns
#%%

df_a2 = df.rename({
'◦ Temperature range (\nC) ': 'T_range', 
' Isobaric specific heat (kJ/kg.K) ': 'Cp',
' Density (kg/m3)': 'mass_density', 
' Thermal conductivity (W/(m.K)) ':'kth',
' Cost factor ($">$/kg) ': 'cost_factor'
}, axis=1)

df_a2.index.name = 'original_name'

# df = df.drop([], axis=1)

df_a2

#%%

df = tables['table_A3']
df.columns

df_a3 = df.rename({
'◦ Temperature range (\nC) ':'T_range', 
' Isobaric specific heat (kJ/kg.K)': 'Cp',
' Density (kg/m3) ': 'mass_density', 
' Thermal conductivity (W/m.K) ':'kth',
' Cost factor ($">$/kg) ':'cost_factor'
}, axis=1)

df_a3.index.name = 'original_name'

df_a3

#%%

df_all = pd.concat([df_a2, df_a3])

#TODO: Need to figure out what this means
df_all = df_all.drop('cost_factor', axis=1)

df_all
df_all['T_range'] = df_all['T_range'].str.replace('--', ' ')
df_all['T_range'] = df_all['T_range'].str.replace('(\d)-(\d)',r'\1 \2', regex=True)

#:TODO manual for Alumina and Magnetite. Need to find a consistent minimum temperature for solid materials...
df_all['T_range'] = df_all['T_range'].str.replace('-1000', '-200 1000')
df_all['T_range'] = df_all['T_range'].str.replace('-1400', '-200 1400')

df_all[['T_melt','T_max']] = df_all['T_range'].str.split(' ', expand=True)

df_all = df_all.dropna(subset= ['T_max'])
df_all = df_all.drop('T_range', axis=1)

df_all['kth'] = df_all['kth'].astype(str).apply(average_range)

df_all['kth'] = df_all['kth'].replace('-',np.nan).replace('nan',np.nan)

df_all['mass_density'] = df_all['mass_density'].astype(str).apply(average_range)
df_all['Cp'] = df_all['Cp'].astype(str).apply(average_range)

df_all


#%%

# Create these files, delete columns other than original_name, then add lookup columns as describd in readme


# df_all.to_csv('SM_lookup.csv')
# df.to_csv('mat_lookup.csv')
#%%

# Setup units for columns 

unit_row = ['kJ/kg/K','kg/m**3', 'W/m/K','degC','degC']
df_all.columns = [df_all.columns, unit_row]

df_all = df_all.pint.quantify(level=-1)



#%%

# Map every column remaining (physical properties) that is not the specific price to the storage medium lookup and output

SM_lookup = pd.read_csv('SM_lookup.csv')

# df_SM = df.drop('specific_price', axis=1)

df_SM = pd.merge(df_all, SM_lookup, on='original_name')
df_SM = df_SM.dropna(subset=['SM_name'])
df_SM = df_SM.set_index('SM_name')


df_SM = convert_units(df_SM)
df_SM = prep_df_pint_out(df_SM)

df_SM.to_csv('output/SM_data.csv')
# %%

