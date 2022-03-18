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
df = df.dropna(subset=['Price'])

df[['min_quantity','min_unit']] = df['min_order'].str.extract("(\S+) ([\S ]+)", expand=True)
df['min_quantity'] = df['min_quantity'].astype(float)

unit_lookup = {
    'Tons': 't',
    'Ton': 't',
    'Metric Tons': 't',
    'Kilogram': 'kg',
}

df['min_unit'] = [unit_lookup[t] if t in unit_lookup else np.nan for t in df['min_unit'].values]
df= df.dropna(subset=['min_unit'])

df['Price'] = df['Price'].str.extract("\$(\S+)")

df['Price'] = df['Price'].str.replace('.00','', regex=False)
df['Price'] = df['Price'].str.replace(',','', regex=False)
df['Price'] = df['Price'].astype(float)

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
df['specific_price'] = df['Price']/df['min_unit_kg']
df

#%%

if not os.path.exists('output'): os.mkdir('output')

df.to_csv('output/processed.csv')

