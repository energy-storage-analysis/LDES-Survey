#%%
import os
import numpy as np
import pandas as pd


# %%
df = pd.read_csv('out.csv')
# df = df.set_index('search_text')

search_lookup = pd.read_csv('keywords.csv', index_col=0)['index']
df.index= [search_lookup[t] for t in df['search_text'].values]
df.index.name = 'index'

df = df.rename({
    'Price': 'price'
},axis=1)

df_single = pd.read_csv('single_manual.csv', index_col=0)
df_single.index.name = 'index'
df_single = df_single[['search_text', 'price', 'min_order']]

df = pd.concat([
    df,
    df_single
])


df = df.dropna(subset=['price'])

df[['min_quantity','min_unit']] = df['min_order'].str.extract("(\S+) ([\S ]+)", expand=True)
df['min_quantity'] = df['min_quantity'].astype(float)

unit_lookup = {
    'Tons': 't',
    'Ton': 't',
    'Metric Tons': 't',
    'Metric Ton': 't',
    'Kilogram': 'kg',
    'Kilograms': 'kg',
}

df['min_unit'] = [unit_lookup[t] if t in unit_lookup else np.nan for t in df['min_unit'].values]
df= df.dropna(subset=['min_unit'])

df['price'] = df['price'].str.extract("\$(\S+)")

df['price'] = df['price'].str.replace('.00','', regex=False)
df['price'] = df['price'].str.replace(',','', regex=False)
df['price'] = df['price'].astype(float)

# %%

import pint
import pint_pandas

ureg = pint.UnitRegistry()


min_quantity_kg = []
min_unit_kg = []
for index, row in df.iterrows():
    unit = row['min_unit']

    val_min_unit = ureg.Quantity(row['min_quantity'], '{}'.format(unit))
    min_quantity_kg.append(val_min_unit.to('kg').magnitude)

    val_1 = ureg.Quantity(1, '{}'.format(unit))
    min_unit_kg.append(val_1.to('kg').magnitude)

    # break
# %%
df['min_quantity_kg'] = min_quantity_kg
df['min_unit_kg'] = min_unit_kg
df
# %%
df['specific_price'] = df['price']/df['min_unit_kg']
df

#%%

if not os.path.exists('output'): os.mkdir('output')

df.to_csv('output/processed.csv')


#%%
df_single = pd.read_csv('single_manual.csv', index_col=0)
isin_single = pd.Series(df.index.isin(df_single.index), index=df.index)

df_t = df.where((df['min_quantity_kg'] > 999) | isin_single).dropna(how='all')


df_t.index.value_counts()
#%%

df_stats = df_t.reset_index().groupby('index').agg({'specific_price':['mean', 'std','count']})['specific_price']


df_stats['ratio'] = df_stats['std']/df_stats['mean']
df_stats['original_name'] = df_t.groupby('index').first()['search_text']
df_stats

#%%

df_prices = df_stats[['mean','original_name']].rename({'mean':'specific_price'}, axis=1)
df_prices.to_csv('output/mat_prices.csv')
