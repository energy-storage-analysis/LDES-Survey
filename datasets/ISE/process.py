#%%
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys


from es_utils.pdf import average_range


# %%

df = pd.read_csv('ISE.csv', encoding='ISO-8859-1', skiprows=[1,2])

df = df.rename({
    'Commodity': 'commodity',
},axis=1)


df.columns = [c.strip() for c in df.columns]

df =df.drop([47,79,81,124]).reset_index(drop=True) # Seems to be a typo for cobalt entry

df['Price in USD'] = df['Price in USD'].apply(average_range)
df['Price in USD'] = df['Price in USD'].astype(float)

df[['currency','mass_unit']] = df['Unit'].str.split(' / ', expand=True)
df['mass_unit'] = df['mass_unit'].astype('string')
# df = df.drop('Unit', axis=1)
df
#%%
df['currency'].value_counts()
#%%
df = df.where(df['currency'] == 'USD').dropna(subset=['currency'])
df
#%%


df['mass_unit'] = df['mass_unit'].replace({
    'lb Co': 'lb',
    'lb VO5': 'lb',
    'lb Ta2O5': 'lb',
    'mt': 'metric_ton',
    't':'metric_ton'
    })

df['mass_unit'].value_counts()
#%%
import pint
import pint_pandas

ureg = pint.UnitRegistry()
ureg.load_definitions('unit_defs.txt')

specific_price = []
for index, row in df.iterrows():
    unit = row['mass_unit']
    val = row['Price in USD']
    val = ureg.Quantity(val, 'USD/{}'.format(unit))
    val = val.to('USD/kg').magnitude
    specific_price.append(val)
    # break

df['specific_price'] = specific_price
# %%
bins = np.logspace(np.log10(0.1), np.log10(1e6), 50)
df['specific_price'].hist(bins=bins)
plt.xscale('log')
plt.xlabel('Cost ($/kg)')
plt.ylabel('Count')
# %%

df['commodity'] = df['commodity'].replace({
    'Ethylene glycol antimony': 'Antimony ethelyene_glycol',
    'polysilicon': 'Silicon polysilicon',
    'Lithium hydroxides monohydrates': 'Lithium hydroxides_monohydrates',
    'Fused cubic zirconia': 'Zirconium fused_cubic',
    'Reduced Ilmenite': 'Ilmenite Reduced'
})

df[['commodity', 'commodity_info']] = df['commodity'].str.split(' ', expand=True)
#%%

df['commodity'].value_counts()

#%%

# df['commodity_info'] = df['commodity_info'].replace({'Conc.': 'Concrete'})
df['original_name'] = df['commodity'] + ' ' + df['commodity_info']


from es_utils.chem import process_chem_lookup

chem_lookup = pd.read_csv('chem_lookup.csv')
chem_lookup = process_chem_lookup(chem_lookup)
df = pd.merge(df, chem_lookup, on='original_name').set_index('index')
# %%

df = df[['material_name','commodity','commodity_info','Specification','specific_price']]

#%%
df.to_csv('output/processed.csv')

# %%
