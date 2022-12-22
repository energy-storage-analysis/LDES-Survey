#%%
import pandas as pd
from es_utils.units import ureg, prep_df_pint_out
from es_utils.pdf import average_range

df = pd.read_csv('input.csv', index_col=0)


df['price'] = df['price'].apply(average_range).astype(float)

#TODO: copied from ISE, consolidate into a function in es_utils
specific_price = []
for index, row in df.iterrows():
    unit = row['price_unit']
    val = row['price']
    val = ureg.Quantity(val, unit)
    val = val.to('USD/kg').magnitude
    specific_price.append(val)
    # break

df['specific_price'] = specific_price
df['specific_price'] = df['specific_price'].astype('pint[USD/kg]')

df_price = df[['molecular_formula','specific_price']]

df_price = prep_df_pint_out(df_price)

df_price.to_csv('output/mat_data.csv')
# %%
