#%%
import pandas as pd
import pint_pandas
from es_utils.units import ureg

df = pd.read_csv('input_data/input.csv', index_col=0)

df = df[['Bid']]


name_dict  = {'GOLD': 'Au', 'SILVER': 'Ag', 'PLATINUM': 'Pt', 'PALLADIUM': 'Pd', 'RHODIUM': 'Rh'}

df = df.rename(name_dict, axis=0)
df = df.rename({'Bid':'specific_price'}, axis=1)
df.index.name = 'index'

df['molecular_formula'] = df.index

df['specific_price'] = df['specific_price'].astype('pint[USD/kg]')

df

#%%
from es_utils.units import prep_df_pint_out

df_out = prep_df_pint_out(df)


#%%


df_out.to_csv('output/mat_data.csv')