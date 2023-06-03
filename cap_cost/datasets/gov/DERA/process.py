
#%%

import pandas as pd

df = pd.read_csv('input_data/input.csv', index_col=0)


# %%
df['price'] = df['price'].str.replace(r'.', '', regex=False).str.replace(',', '.')

df['price'] = df['price'].astype(float)
# %%

df['price_unit'] = df['price_unit'].str.replace(r'US$', 'USD', regex=False)
df['price_unit'] = df['price_unit'].str.replace(r'€', 'EUR', regex=False)
df['price_unit'] = df['price_unit'].str.replace('dmtu', 'metric_ton') 
df['price_unit'] = df['price_unit'].str.replace('mtu', 'metric_ton') 
df['price_unit'] = df['price_unit'].str.replace('troz', 'troy_ounce') 
df['price_unit'] = df['price_unit'].str.replace('RMB', 'CNY') 
# df['price_unit'] = df['price_unit'].str.replace('US$', 'USD')
#%%

# We drop SMM because it is already being used as a primary source. 
df = df.where(df['source'] != 'SMM').dropna(how='all')

# from pint import Quantity
from es_utils.units import ureg

pqs = []
for idx, row in df.iterrows():
    pq = ureg.Quantity(row['price'], row['price_unit'])
    pq = pq.to('USD/kg').magnitude
    pqs.append(pq)


df['specific_price'] = pqs
df['specific_price'] = df['specific_price'].astype('pint[USD/kg]')

df
# %%

#Years are all the same (2022) so no need to include them. 
df = df[['original_name', 'specific_price']]

#%%

from es_utils.units import prep_df_pint_out


df_out = prep_df_pint_out(df)

df_out.to_csv('output/mat_data.csv')


# %%
