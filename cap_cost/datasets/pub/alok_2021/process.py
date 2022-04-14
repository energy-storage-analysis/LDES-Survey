#%%
import pandas as pd
import os
SM_lookup = pd.read_csv('SM_lookup.csv', index_col=0)

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


df_table12_mix = pd.read_csv('tables/table_12_mix.csv', index_col=0)

df_table12_mix = df_table12_mix.rename({
    'Latent Heat (J/g)': 'sp_latent_heat',
    'Melting Point (°C)': 'phase_change_T',
}, axis=1)

df_table12_mix['sp_latent_heat'] = df_table12_mix['sp_latent_heat']/3600


#%%
df = pd.concat([
    df_table12,
    df_table13
])




import es_utils
chem_lookup = pd.read_csv('chem_lookup.csv')
chem_lookup = es_utils.chem.process_chem_lookup(chem_lookup)
df = pd.merge(df, chem_lookup, on='original_name')

df_prices = es_utils.extract_df_mat(df.set_index('index'))
df_prices.to_csv('output/mat_data.csv')

#%%

df_single = df.set_index('original_name')[['sp_latent_heat','phase_change_T', 'molecular_formula']]

df_single = df_single.drop('molecular_formula', axis=1)

df_SMs = pd.concat([
    df_single, 
    df_table12_mix
])


# df_SMs['SM_type'] = 'latent_thermal'
# df_SMs = df_SMs
#No SM lookup needed as SM are just just the materials

df_SMs
#%%
df_SMs = pd.merge(df_SMs, SM_lookup, on='original_name')

df_SMs = df_SMs.set_index('SM_name')

df_SMs

#%%

# df_SMs['SM_type'] = 'latent_thermal'
df_SMs = df_SMs[['sp_latent_heat','phase_change_T','materials','mat_basis','SM_type']]
# df_SMs = df_SMs.rename({'molecular_formula': 'materials'}, axis=1) #All signle materia molecular form

# df_SMs.index.name = 'SM_name'

df_SMs = df_SMs.dropna(subset=['materials'])

df_SMs.to_csv('output/SM_data.csv')


# %%
