#%%

import pandas as pd
from es_utils.units import ureg

df = pd.read_csv('input_data/input.csv', index_col=0)
df['price'] = df['price'].str.replace("$",'')

df[['price_low', 'price_hieh']] = df['price'].str.split('-', expand=True)


# all units are in grams
# Because this is already a low quantity item already, just take the low price( highest volume)
df['specific_price'] = df['price_low'].astype(float)*1000

df

# %%
df_out = df.groupby('index')['specific_price'].mean().to_frame()


df_out['specific_price'] = df_out['specific_price'].astype('pint[USD/kg]')

#%%

from es_utils.units import prep_df_pint_out

df_out = prep_df_pint_out(df_out)

df_out.to_csv('output/mat_data.csv')
# %%
