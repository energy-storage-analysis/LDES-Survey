#%%
import pandas as pd
from es_utils.units import ureg, convert_units

SM_lookup = pd.read_csv('SM_lookup.csv', index_col=0)

df_table12 = pd.read_csv('tables/table_12_single.csv', index_col=0)

#I am not sure exatly what the other 'latent heat' entry is in the table (booiling?)
df_table12 = df_table12.rename({
    'Heat of fusion (J/g)': 'sp_latent_heat',
    'Melting point (°C)': 'phase_change_T',
    'Cost ($/tonne)': 'specific_price',
}, axis=1)

df_table12['specific_price'] = df_table12['specific_price'].str.replace(',','.',regex=False)
df_table12['specific_price'] = df_table12['specific_price'].astype(float)

df_table12 = df_table12.astype({
    'sp_latent_heat': 'pint[J/g]', 
    'phase_change_T': 'pint[degC]',
    'specific_price': 'pint[USD/ton]'
    })

df_table12 = convert_units(df_table12)

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


df_table13 = df_table13.astype({
    'sp_latent_heat': 'pint[MJ/kg]', 
    'phase_change_T': 'pint[degC]',
    'specific_price': 'pint[USD/lb]'
    })


df_table13 = convert_units(df_table13)

df_table13 = df_table13[['sp_latent_heat','specific_price', 'phase_change_T']]

#%%


df_table12_mix = pd.read_csv('tables/table_12_mix.csv', index_col=0)

df_table12_mix = df_table12_mix.rename({
    'Latent Heat (J/g)': 'sp_latent_heat',
    'Melting Point (°C)': 'phase_change_T',
}, axis=1)

df_table12_mix = df_table12_mix.astype({
    'sp_latent_heat': 'pint[J/g]', 
    'phase_change_T': 'pint[degC]',
    })

df_table12_mix = convert_units(df_table12_mix)


#%%
df = pd.concat([
    df_table12,
    df_table13
])

import es_utils
chem_lookup = pd.read_csv('chem_lookup.csv')
chem_lookup = es_utils.chem.process_chem_lookup(chem_lookup)
df = pd.merge(df, chem_lookup, on='original_name')
df = df.set_index('index')


df_prices = es_utils.extract_df_mat(df)

from es_utils.units import prep_df_pint_out

df_prices = prep_df_pint_out(df_prices)
# df_prices = df_prices.set_index('index')
df_prices.to_csv('output/mat_data.csv')

#%%

df_single = df.set_index('original_name')[['sp_latent_heat','phase_change_T', 'molecular_formula']]

df_single = df_single.drop('molecular_formula', axis=1)

df_SMs = pd.concat([
    df_single, 
    df_table12_mix
])

#%%
df_SMs = pd.merge(df_SMs, SM_lookup, on='original_name')

df_SMs = df_SMs.set_index('SM_name')

df_SMs = df_SMs[['sp_latent_heat','phase_change_T','materials','mat_basis','SM_type']]
df_SMs = df_SMs.dropna(subset=['materials'])

df_SMs = prep_df_pint_out(df_SMs)

df_SMs.to_csv('output/SM_data.csv')