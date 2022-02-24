#%%

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import pint
ureg = pint.UnitRegistry()
ureg.load_definitions('unit_defs.txt')



# %%
df = pd.read_csv('data/prices.csv', index_col=0)
df = df.dropna(subset=['price'])
df

df = df.where(df['price_units'] != 'Index').dropna(subset=['price_units']) #TODO: how to deal with consumer price index

df['price_units'] = df['price_units'].replace({
    'ctslb': 'cents/lb',
    'dt': 'USD/ton',
    'dkg' : 'USD/kg',
    'dg': 'USD/g',
    'dlb':'USD/lb',
    'dto':'USD/ton',
    't':'USD/ton',
    'dct':'USD/carat',
    'dtoz':'USD/toz',
    'dst': 'USD/short_ton',
    'df':'USD/flask',
    'kg': 'USD/kg'
})

df['price_units'].value_counts()


price_per_kg = []
for index, row in df.iterrows():
    unit = row['price_units']
    val = row['price']
    val = ureg.Quantity(val, unit)
    val = val.to('USD/kg').magnitude
    price_per_kg.append(val)

df['price_per_kg'] = price_per_kg


# %%
bins = np.logspace(np.log10(0.1), np.log10(1e6), 50)
df['price_per_kg'].hist(bins=bins)
plt.xscale('log')

#%%
df_high = df.where(df['price_per_kg'] >1e3).dropna()
df_high[['Commodity','price_per_kg']].sort_values('price_per_kg')
#%%
df_low = df.where(df['price_per_kg'] <10).dropna()
df_low.sort_values('price_per_kg').iloc[0:50]
# %%
avg_price = df.groupby('Commodity')['price_per_kg'].mean()
avg_price = avg_price.sort_values()
avg_price.name = 'average_price'
avg_price.iloc[0:50]

# %%
bins = np.logspace(np.log10(0.1), np.log10(1e6), 50)
avg_price.hist(bins=bins)
plt.xscale('log')
plt.xlabel('Cost ($/kg)')
plt.ylabel('Count')

#%%
std_price = df.groupby('Commodity')['price_per_kg'].std()
std_price = std_price.sort_values()
std_price.name = 'stddev_price'
# %%
commodity_counts = df['Commodity'].sort_values(ascending=False).value_counts()
commodity_counts.name = 'num_entries'

df_commodity = pd.concat([
    commodity_counts,
    avg_price,
    std_price 
], axis=1)
df_commodity
#%%

df_commodity['ratio'] = df_commodity['stddev_price']/df_commodity['average_price']

df_commodity.sort_values('ratio', ascending=False)
#%%


df_commodity['formula'] = ''
df_commodity.to_csv('data/commodity.csv')

# %%
