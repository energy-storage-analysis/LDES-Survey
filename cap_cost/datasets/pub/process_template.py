"""
Processing script template. This template is designed to work on extracted data (e.g. tables from pdf obtained from extract_template.py)
"""

#%%
import pandas as pd
import os
from es_utils.units import prep_df_pint_out, convert_units
from es_utils.chem import process_chem_lookup

if not os.path.exists('output'): os.mkdir('output')
tables = {fn.strip('.csv') : pd.read_csv(os.path.join('tables',fn), encoding='utf-8', index_col=0) for fn in os.listdir('tables')}
#%%

# Output the columns of a table into the Ipython console and copy to the rename dictonary below to rename the columns. 

df = tables['table_1']
df.columns
#%%

df = df.rename({

}, axis=1)

df.index.name = 'original_name'
# df = df.drop([], axis=1)

df


#%%

# Create these files, delete columns other than original_name, then add lookup columns as describd in readme


# df.to_csv('SM_lookup.csv')
# df.to_csv('mat_lookup.csv')
#%%

# Setup units for columns 

unit_row = ['degC','degC', 'kJ/kg/K','W/m/K','USD/kg','USD/kWh']
df.columns = [df.columns, unit_row]

df = df.pint.quantify(level=-1)



#%%

# Map every column remaining (physical properties) that is not the specific price to the storage medium lookup and output

SM_lookup = pd.read_csv('SM_lookup.csv')

df_SM = df.drop('specific_price', axis=1)

df_SM = pd.merge(df_SM, SM_lookup, on='original_name')
df_SM = df_SM.dropna(subset=['SM_name'])
df_SM = df_SM.set_index('SM_name')


df_SM = convert_units(df_SM)
df_SM = prep_df_pint_out(df_SM)

df_SM.to_csv('output/SM_data.csv')
# %%

# Map specific price to the mat lookup and output

df.index.name = 'original_name'

mat_lookup = pd.read_csv('mat_lookup.csv')
mat_lookup = process_chem_lookup(mat_lookup)


df_mat = df[['specific_price']]

df_mat = pd.merge(df_mat, mat_lookup, on='original_name')
df_mat = df_mat.dropna(subset=['index'])
df_mat = df_mat.set_index('index')

df_mat = convert_units(df_mat)
df_mat = prep_df_pint_out(df_mat)


df_mat.to_csv('output/mat_data.csv')
# %%
