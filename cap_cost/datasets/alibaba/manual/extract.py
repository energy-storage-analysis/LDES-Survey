#%%
import os
from re import search
import numpy as np
import pandas as pd



#%%


df_single = pd.read_csv('single_manual.csv')
# df_single.index.name = 'index'
df_single = df_single[['index','search_text', 'price', 'min_order','molecular_formula', 'Title','link']].set_index('search_text')


single_data_lookup = df_single.reset_index()[['search_text', 'molecular_formula']]


df = df_single

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

df = df[[
'Title','specific_price','min_quantity_kg','index','molecular_formula','link','min_quantity','min_unit'
]]


if not os.path.exists('output'): os.mkdir('output')

df.to_csv('output/extracted.csv')



# %%

# %%
