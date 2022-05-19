#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from es_utils.pdf import average_range
from es_utils.units import convert_units, prep_df_pint_out, ureg

df = pd.read_csv('ISE.csv', encoding='ISO-8859-1')

df = df.rename({
    'Price in USD': 'price',
},axis=1)


df.columns = [c.strip() for c in df.columns]

df =df.drop([47,79,81,124]).reset_index(drop=True) # Seems to be a typo for cobalt entry

df['price'] = df['price'].apply(average_range)
df['price'] = df['price'].astype(float)

df[['currency','mass_unit']] = df['Unit'].str.split(' / ', expand=True)
df['mass_unit'] = df['mass_unit'].astype('string')

#%%
df = df.where(df['currency'] == 'USD').dropna(subset=['currency'])

df['mass_unit'] = df['mass_unit'].replace({
    'lb Co': 'lb',
    'lb VO5': 'lb',
    'lb Ta2O5': 'lb',
    'mt': 'metric_ton',
    't':'metric_ton'
    })

specific_price = []
for index, row in df.iterrows():
    unit = row['mass_unit']
    val = row['price']
    val = ureg.Quantity(val, 'USD/{}'.format(unit))
    val = val.to('USD/kg').magnitude
    specific_price.append(val)
    # break

df['specific_price'] = specific_price


df = df.astype({
    'specific_price': 'pint[USD/kg]'
})
# %%

df['original_name'] = df['original_name'].replace({
    'Ethylene glycol antimony': 'Antimony ethelyene_glycol',
    'polysilicon': 'Silicon polysilicon',
    'Lithium hydroxides monohydrates': 'Lithium hydroxides_monohydrates',
    'Fused cubic zirconia': 'Zirconium fused_cubic',
    'Reduced Ilmenite': 'Ilmenite Reduced'
})

df[['original_name', 'commodity_info']] = df['original_name'].str.split(' ', expand=True)
#%%

df['original_name'] = df['original_name'] + ' ' + df['commodity_info']

from es_utils.chem import process_chem_lookup

chem_lookup = pd.read_csv('chem_lookup.csv')
chem_lookup = process_chem_lookup(chem_lookup)
df = pd.merge(df, chem_lookup, on='original_name')


df.to_csv('output/processed.csv', index=False)

# %%

df_combine = df.groupby('index')[['specific_price']].mean()

from es_utils import join_col_vals
df_combine['original_name']= df.groupby('index')['original_name'].apply(join_col_vals)
df_combine['molecular_formula']= df.groupby('index')['molecular_formula'].apply(join_col_vals)

from es_utils import extract_df_mat
df_price = extract_df_mat(df_combine)

#%%

from es_utils.chem import calc_hydrate_factor

hydrate_list = [
    ('LiOH(H2O)', 'LiOH', 1),
]

for hydrate_formula, anhydrous_formula, hydrate_count in hydrate_list:
    df_price.loc[hydrate_formula,'specific_price'] = df_price.loc[hydrate_formula,'specific_price']*calc_hydrate_factor(anhydrous_formula, hydrate_count)

    df_price.loc[hydrate_formula,'molecular_formula'] = anhydrous_formula
    df_price = df_price.rename({hydrate_formula: anhydrous_formula})
#%%


df_price = prep_df_pint_out(df_price)

df_price.to_csv('output/mat_data.csv')
