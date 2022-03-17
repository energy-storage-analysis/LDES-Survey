#%%
import pandas as pd
import os

#TODO: process salt mixture table
df_table12 = pd.read_csv('tables/table_12_single.csv', index_col=0)

#I am not sure exatly what the other 'latent heat' entry is in the table (booiling?)
df_table12 = df_table12.rename({
    'Heat of fusion (J/g)': 'sp_latent_heat',
    'Melting point (°C)': 'phase_change_T',
    'Cost ($/tonne)': 'specific_price',
}, axis=1)

df_table12['sp_latent_heat'] = df_table12['sp_latent_heat']/3600


df_table12['specific_price'] = df_table12['specific_price'].str.replace(',','.',regex=False)
df_table12['specific_price'] = df_table12['specific_price'].astype(float)
df_table12['specific_price'] = df_table12['specific_price']/1000

df_table12 = df_table12[['sp_latent_heat','specific_price']]

#%%

df_table13 = pd.read_csv('tables/table_13.csv', index_col=0)

df_table13 = df_table13.rename({
    'Latent Heat (MJ/kg)': 'sp_latent_heat',
    'Melting Point (°C)': 'phase_change_T',
    'Cost ($/lb)': 'specific_price'
}, axis=1)

from es_utils.pdf import average_range

df_table13['specific_price'] = df_table13['specific_price'].astype(str).apply(average_range).astype(float)

df_table13['sp_latent_heat'] = df_table13['sp_latent_heat']/3.600

df_table13 = df_table13[['sp_latent_heat','specific_price', 'phase_change_T']]

#%%
df = pd.concat([
    df_table12,
    df_table13
])

df['energy_type'] = 'latent_thermal'

df

#%%



#%%
import es_utils
chem_lookup = pd.read_csv('chem_lookup.csv')
chem_lookup = es_utils.chem.process_chem_lookup(chem_lookup)
df = pd.merge(df, chem_lookup, on='original_name').set_index('index')

from es_utils import extract_df_physprop, extract_df_price
df_physprop = es_utils.extract_df_physprop(df, physprops=['sp_latent_heat','phase_change_T'])

df_prices = es_utils.extract_df_price(df)

df_prices.to_csv('output/mat_prices.csv')
df_physprop.to_csv('output/physprop.csv')


# %%
