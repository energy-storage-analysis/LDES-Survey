#%%
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

sys.path.append('..')
from pdf_utils import average_range


# %%

df = pd.read_csv('ISE.csv', encoding='ISO-8859-1', skiprows=[1,2])
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
    'lb Ta2O5': 'lb'
    })

df['mass_unit'].value_counts()
#%%
import pint
import pint_pandas

ureg = pint.UnitRegistry()
ureg.load_definitions('unit_defs.txt')

price_per_kg = []
for index, row in df.iterrows():
    unit = row['mass_unit']
    val = row['Price in USD']
    val = ureg.Quantity(val, 'USD/{}'.format(unit))
    val = val.to('USD/kg').magnitude
    price_per_kg.append(val)

df['price_per_kg'] = price_per_kg
# %%
bins = np.logspace(np.log10(0.1), np.log10(1e6), 50)
df['price_per_kg'].hist(bins=bins)
plt.xscale('log')
plt.xlabel('Cost ($/kg)')
plt.ylabel('Count')
# %%

df['Commodity'] = df['Commodity'].replace({
    'Ethylene glycol antimony': 'Antimony ethelyene_glycol',
    'polysilicon': 'Silicon polysilicon',
    'Lithium hydroxides monohydrates': 'Lithium hydroxides_monohydrates',
    'Fused cubic zirconia': 'Zirconium fused_cubic',
    'Reduced Ilmenite': 'Ilmenite Reduced'
})

df[['material', 'type']] = df['Commodity'].str.split(' ', expand=True)
#%%

df['material'].value_counts()
# %%
