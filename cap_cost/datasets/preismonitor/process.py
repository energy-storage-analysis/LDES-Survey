
#%%

import pandas as pd

df = pd.read_csv('output/extracted.csv', index_col=0)

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

df = df[['original_name', 'specific_price']]

#%%

from es_utils.units import prep_df_pint_out


df_out = prep_df_pint_out(df)

df_out.to_csv('output/mat_data.csv')


# %%
