#%%
import os
from re import search
import numpy as np
import pandas as pd


# %%
df = pd.read_csv('out_bulk.csv', index_col=0)

df = df.drop(['CFRP AS4-3501â€“6', 'CFRP IM7-8551â€“7', 'CFRP IM7â€“8552'])
# df = df.set_index('search_text')
df
#%%
search_lookup = pd.read_csv('keywords_bulk.csv').set_index('search_text')[['index', 'molecular_formula']]
# df.index= [search_lookup['index'][t] for t in df.index]
# df.index.name = 'index'
search_lookup

search_lookup

df['index'] = search_lookup.loc[df.index]['index'].values
df['molecular_formula'] = search_lookup.loc[df.index]['molecular_formula'].values

df

# #%%
# df_single = pd.read_csv('single_manual.csv', index_col=0)
# df_single.index.name = 'index'



# single_data_lookup = df_single[['search_text', 'molecular_formula']].reset_index().set_index('search_text')
# single_data_lookup.index.name = 'keyword'
# search_lookup = pd.concat([search_lookup, single_data_lookup])

# df_single = df_single[['search_text', 'price', 'min_order', 'molecular_formula']]

# df_single = df_single.reset_index().set_index('search_text')

# df_single
# #%%

# #%%
# df = pd.concat([
#     df,
#     df_single
# ])

# df




# df_keywords = pd.read_csv('keywords_allmats.csv').set_index('search_text')
#%%


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
df

#%%
df= df.dropna(subset=['min_unit'])

df['price'] = df['price'].str.extract("\$(\S+)")

df['price'] = df['price'].str.replace('.00','', regex=False)
df['price'] = df['price'].str.replace(',','', regex=False)
df['price'] = df['price'].astype(float)

#%%


df
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


df = df[[
'title','specific_price','min_quantity_kg','index','molecular_formula','link','min_quantity','min_unit'
]]


df.to_csv('output/extracted.csv')


#%%
