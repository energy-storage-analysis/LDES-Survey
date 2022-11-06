#%%

import os

import numpy as np
import pandas as pd
import pint
import pint_pandas

from es_utils.units import ureg


df = pd.read_json('output/items.jl', lines=True).set_index('index')



df_single_manual = pd.read_csv('single_manual.csv', index_col=0)
df_single_manual

df = pd.concat([
    df,
    df_single_manual,
])

#We drop duplicate titles, I believe only relevant for when items.jl is formed from multiple iterations.
df = df.drop_duplicates(subset='title', keep='first')


df['price'] = df['price'].str.replace(' /', '')

# df = df.dropna(subset=['price'])

#TODO: Do any entries have price as USD? 
df = df.where(df['price'].str.contains('₹')).dropna(subset=['price'])

df['price'] = df['price'].str.replace("₹", '')
df['price'] = df['price'].str.replace(",", '')
# df['price'] = df['price'].astype(float)

# df['price'] = df['price']

df['price'] = df['price'].astype("pint[INR]")
df['price'] = df['price'].pint.to('USD')

df['price']

#%%

df['price_amount'] = df['price_amount'].astype(str)
df['price_amount']



#%%


#%%
# df[['min_quantity','min_unit']] = df['min_order'].str.extract("(\S+) ([\S ]+)", expand=True)
# df['min_quantity'] = df['min_quantity'].astype(float)

#TODO: This is effectively inducing a cutoff of > 1kg as grams are not included. This should be implemented explicitly. 
unit_lookup = {
    'Tons': 't',
    'Ton': 't',
    'Metric Tons': 't',
    'Metric Ton': 't',
    'Kilogram': 'kg',
    'Kilograms': 'kg',
    'Kg': 'kg'
}

df['price_amount'] = [unit_lookup[t] if t in unit_lookup else np.nan for t in df['price_amount'].values]



#%%

df= df.dropna(subset=['price_amount'])

# ureg = pint.UnitRegistry()



prices_unit = []
for index, row in df.iterrows():
    unit = row['price_amount']
    unit = ureg.Quantity(1, unit)

    price_unit = row['price']/unit
    price_unit = price_unit.to('USD/kg').magnitude
    prices_unit.append(price_unit)


    # break

prices_unit
# df['min_quantity_kg'] = min_quantity_kg
# df['min_unit_kg'] = min_unit_kg
# df['specific_price'] = df['price']/df['min_unit_kg']

df['specific_price'] = prices_unit
df['specific_price'] = df['specific_price']#.astype('pint[USD/kg]')

df['specific_price']

#%%


# from es_utils.chem import calc_hydrate_factor

# scaled_prices = []
# hydrate_counts = []
# for anhydrous_formula, row in df.iterrows():
#     if row['split_hydrate']:

#         #Check title for matching hydrate strings, ideally only one. 
#         matching_n = []
#         for n, prefix in hydrate_lookup.items():
#             if prefix in row['title'].lower():
#                 matching_n.append(n)
#         if len(matching_n) == 1:
#             hydrate_count = matching_n[0]
#         elif len(matching_n) == 0:  
#             hydrate_count = 'not_specified'
#         else:
#             hydrate_count = 'multiple_found'

#         hydrate_counts.append(hydrate_count)

#         #Price is only scaled for integer hydrate count
#         if isinstance(hydrate_count, int):
#             price_factor = calc_hydrate_factor(anhydrous_formula, hydrate_count)
#             scaled_price = row['specific_price']*price_factor
#             scaled_prices.append(scaled_price)
#         else:
#             scaled_prices.append(np.nan)

#     else:
#         scaled_prices.append(np.nan)
#         hydrate_counts.append(np.nan)

# df['scaled_anhydrous_price'] = scaled_prices
# df['hydrate_count'] = hydrate_counts

df['keep'] = 'y' #This is to be edited for removing entries

df = df[[
'specific_price','keep','title','link','search_text',
]]

df = df.sort_index()

df.to_csv('output/extracted.csv')
