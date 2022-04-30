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



df[['price_low','price_high']] = df['price'].str.split('-', expand=True)

#TODO: Just taking the low price for now, as that should be associated with the largest minimum order quantity. Evenyually the scraping sider should be improved to actually look at the product page and get the price as function of order quantiy
df = df.drop('price',axis=1).rename({
    'price_low': 'price'
}, axis=1)

# df['price']


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


from es_utils.chem import get_molecular_mass

# Form hydrated formulas, no conversion. The code in the pipeline determining hydrate count should perhaps go here. 
# df['hydrate_count'] = df['hydrate_count'].replace('not_specified', 0).astype(float)


scaled_prices = []
hydrate_counts = []
for idx, row in df.iterrows():
    if row['split_hydrate']:
        matching_n = []
        for n, prefix in hydrate_lookup.items():
            if prefix in row['title'].lower():
                matching_n.append(n)
        if len(matching_n) == 0:
            hydrate_count = 0 #TODO: Assume missing in title in anydrous...
        elif len(matching_n) == 1:
            hydrate_count = matching_n[0]
        else:
            hydrate_count = np.nan

        hydrate_counts.append(hydrate_count)

        if hydrate_count == hydrate_count:
            hydrate_count = int(hydrate_count)
            if hydrate_count > 0:
                mu = get_molecular_mass(idx)
                mu_water = get_molecular_mass('H2O')*hydrate_count

                price_factor = (mu+mu_water)/mu
                scaled_price = row['specific_price']*price_factor
                scaled_prices.append(scaled_price)
            else:
                scaled_prices.append(np.nan)
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

