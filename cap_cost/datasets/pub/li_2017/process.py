#%%
import numpy as np
import pandas as pd
from es_utils.chem import process_chem_lookup
from es_utils.units import convert_units, prep_df_pint_out, ureg

chem_lookup = pd.read_csv('chem_lookup.csv')
chem_lookup = process_chem_lookup(chem_lookup)
# %%
table_3 = pd.read_csv('tables/table_3.csv', index_col=0)

added_rows = pd.DataFrame({
    'molecular_formula': ['O2'],
    'ref': [np.nan],
    'specific_price': [0]
}, index = ['Air'])
added_rows.index.name ='index'

table_3 = pd.merge(table_3, chem_lookup, on='original_name').set_index('index')
table_3 = table_3.append(added_rows)
#%%

from es_utils.chem import calc_hydrate_factor

hydrate_list = [
    ('CrCl3(H2O)6', 'CrCl3', 6),
    ('LiOH(H2O)', 'LiOH', 1),
    ('NiCl2(H2O)6', 'NiCl', 6),
    ('VOSO4(H2O)4', 'VOSO4', 4),
    ('ZnSO4(H2O)7', 'ZnSO4', 7)
]

for hydrate_formula, anhydrous_formula, hydrate_count in hydrate_list:
    table_3.loc[hydrate_formula,'specific_price'] = table_3.loc[hydrate_formula,'specific_price']*calc_hydrate_factor(anhydrous_formula, hydrate_count)
    table_3.loc[hydrate_formula,'molecular_formula'] = anhydrous_formula
    table_3 = table_3.rename({hydrate_formula: anhydrous_formula})

# %%

from es_utils import extract_df_mat
df_price = extract_df_mat(table_3)

df_price = df_price.astype({
    'specific_price': 'pint[USD/kg]',
    })
df_price = convert_units(df_price)
df_price = prep_df_pint_out(df_price)


df_price.to_csv('output/mat_data.csv')

#%%
df = pd.read_csv('tables/table_2.csv')
df = df.rename({'C_kwh': 'C_kwh_orig'}, axis=1)
df = df.dropna(how='all')
df = df.drop('ref',axis=1)
df = df.rename({'label':'original_name'}, axis=1).set_index('original_name')
# %%

SM_lookup = pd.read_csv('SM_lookup.csv', index_col=0)

df_SM = pd.merge(df, SM_lookup, on='original_name')

# df_SM.index.name = 'SM_name'
df_SM = df_SM.reset_index(drop=True).set_index('SM_name') #Dropping original name as it is so similar

df_SM = df_SM[['C_kwh_orig','sub_type','deltaV','n_e','materials','mat_basis','SM_type']]

df_SM = df_SM.astype({
    'deltaV': 'pint[V]',
    'n_e': 'pint[dimensionless]',
    'C_kwh_orig': 'pint[USD/kWh]',
    })

df_SM = convert_units(df_SM)
df_SM = prep_df_pint_out(df_SM)

df_SM.to_csv('output/SM_data.csv')


