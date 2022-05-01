#%%

import os

import numpy as np
import pandas as pd
import pint

hydrate_lookup = {
    0: 'anhydr',
    1 : 'monohydr',
    2 : 'dihydr',
    3 : 'trihydr',
    4 : 'tetrahydr',
    5 : 'pentahydr',
    6 : 'hexahydr',
    7 : 'heptahydr',
    8 : 'octahydr'
}


df = pd.read_json('output/items.jl', lines=True).set_index('index')

#We drop duplicate titles, I believe only relevant for when items.jl is formed from multiple iterations.
df = df.drop_duplicates(subset='title', keep='first')

#%%
df[['price_normal_low','price_normla_high']] = df['price_normal'].str.split('-', expand=True)

#Take the lower normal price (as that would be the largest quantity available in the min_order unit) if exists other wise take the promotion price
#TODO: The returned type of price seems random. Need to rexamine hte 'promotion price'
df['price'] = df['price_normal_low'].fillna(df['price_promotion'])




#%%
df[['min_quantity','min_unit']] = df['min_order'].str.extract("(\S+) ([\S ]+)", expand=True)
df['min_quantity'] = df['min_quantity'].astype(float)

#TODO: This is effectively inducing a cutoff of > 1kg as grams are not included. This should be implemented explicitly. 
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

df['min_quantity_kg'] = min_quantity_kg
df['min_unit_kg'] = min_unit_kg
df['specific_price'] = df['price']/df['min_unit_kg']

#%%


from es_utils.chem import calc_hydrate_factor

scaled_prices = []
hydrate_counts = []
for anhydrous_formula, row in df.iterrows():
    if row['split_hydrate']:

        #Check title for matching hydrate strings, ideally only one. 
        matching_n = []
        for n, prefix in hydrate_lookup.items():
            if prefix in row['title'].lower():
                matching_n.append(n)
        if len(matching_n) == 1:
            hydrate_count = matching_n[0]
        elif len(matching_n) == 0:  
            hydrate_count = 'not_specified'
        else:
            hydrate_count = 'multiple_found'

        hydrate_counts.append(hydrate_count)

        #Price is only scaled for integer hydrate count
        if isinstance(hydrate_count, int):
            price_factor = calc_hydrate_factor(anhydrous_formula, hydrate_count)
            scaled_price = row['specific_price']*price_factor
            scaled_prices.append(scaled_price)
        else:
            scaled_prices.append(np.nan)

    else:
        scaled_prices.append(np.nan)
        hydrate_counts.append(np.nan)

df['scaled_anhydrous_price'] = scaled_prices
df['hydrate_count'] = hydrate_counts



df = df[[
'specific_price','min_quantity_kg','hydrate_count','scaled_anhydrous_price','title','link','min_quantity','min_unit','search_text',
]]

df.to_csv('output/extracted.csv')
