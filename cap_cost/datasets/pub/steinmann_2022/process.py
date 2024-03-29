#%%
import pandas as pd
import numpy as np
import os
from es_utils.pdf import average_range
from es_utils.units import convert_units, prep_df_pint_out, ureg
from es_utils.chem import process_mat_lookup

if not os.path.exists('output'): os.mkdir('output')
tables = {fn.strip('.csv') : pd.read_csv(os.path.join('tables',fn), encoding='utf-8', index_col=0) for fn in os.listdir('tables')}
#%%

SM_lookup = pd.read_csv('SM_lookup.csv')

mat_lookup = pd.read_csv('mat_lookup.csv')
mat_lookup = process_mat_lookup(mat_lookup)



#%%
df_t21 = tables['table_21']

df_t21 = df_t21.rename({
'Temperature range [°C]': "T_range", 
'Spec Heat capacity [J/kgK]': 'Cp',
'Density [kg/m3] ': 'mass_density', 
'Estimated Material cost [€/ton]': 'specific_price'
}, axis=1)

df_t21.index.name = 'original_name'

df_t21['specific_price'] = df_t21['specific_price'].fillna('').apply(average_range).replace('',np.nan).astype(float)

df_t21['T_range'] = df_t21['T_range'].str.replace('\n','').str.replace('°C','')

df_t21[['T_melt', 'T_max']] = df_t21['T_range'].str.split('-', expand=True)[[0,1]]

df_t21 = df_t21.drop('T_range', axis=1)

df_t21 = pd.concat([
df_t21.iloc[1:4],#.assign(Type='Molten Salt'),
df_t21.iloc[7:8],#.assign(Type='Liquid Metals'),
df_t21.iloc[10:11],#.assign(Type='Mineral Oil'),
df_t21.iloc[12:13],#.assign(Type='Synthetic Liquid'),
df_t21.iloc[14:15],#.assign(Type='Element'),
df_t21.iloc[16:17]#.assign(Type='Vegetable oil'),
])

#These are named different in each table...
df_t21 = df_t21.rename({
    "KNO3-NaNO3 [Solar Salt, Draw salt,": 'Solar Salt',
    "Partherm 430]\nNaNO2-KNO3-NaNO3 [Heat transfer": 'HITEC',
    "salt (HTS), HITEC-HTS (Coastal": 'HITEC XL',
    "Therminol VP1\n(vapor pressure at 400 °C: 10.9 bar)": 'Therminol VP1'
    })

#%%
df_t23 = tables['table_23']

df_t23 = df_t23.rename({
'Maximum\nTemperature Difference ∆Tmax [K]': 'deltaT_max',
}, axis=1)

df_t23.index.name = 'original_name'

df_t23 = df_t23[['deltaT_max']]

df_t23 = df_t23.iloc[[1,2,3,5,6,8,10,12]]

df_t23 = df_t23.rename({
    "KNO3-NaNO3 Solar Salt": 'Solar Salt',
    "NaNO2-KNO3-NaNO3 \nHeat Transfer Salt (HTS)": 'HITEC',
    "KNO3-NaNO3-Ca(NO3)2": 'HITEC XL'
    })


#%%
df_liquid = pd.concat([df_t21, df_t23], axis=1)
df_liquid = df_liquid[['Cp', 'mass_density','T_melt', 'T_max', 'deltaT_max','specific_price']]
df_liquid

#TODO: Move to data extraction, incorrectly extracted as +10 degC
df_liquid.loc['Mobiltherm 605', 'T_melt'] = -10

df_liquid = df_liquid.astype({
    'T_melt': 'pint[degC]',
    'T_max': 'pint[degC]',
    'deltaT_max': 'pint[delta_degC]',
    'Cp': 'pint[J/kg/K]',
    'mass_density': 'pint[kg/m**3]',
    'specific_price': 'pint[EUR/metric_ton]',
    })

#%%
df_t31 = tables['table_31']

df_t31 = df_t31.rename({
'Storage Medium  ': 'original_name', 
'Maximal Temperature [°C]': 'T_max',
'Spec Heat capacity [J/kgK]': 'Cp', 
'Density [kg/m3] ': 'mass_density',
'Estimated Material cost\n[€/ton]': 'specific_price'
}, axis=1)

df_t31 = df_t31.reset_index(drop=True).set_index('original_name')
df_t31 = df_t31.dropna()

df_t31['Cp'] = df_t31['Cp'].apply(average_range)
df_t31['T_max'] = df_t31['T_max'].apply(average_range)

df_t31['specific_price'] = df_t31['specific_price'].str.replace('< 50','0-50') #TODO: Tables just say < 50, which I will take as a range from 0-50, or an estimate price of 25$/ton. This should perhaps just be dropped but should look through text more if there is a source for this. 
df_t31['specific_price'] = df_t31['specific_price'].apply(average_range)




#%%
df_t32 = tables['table_32']

df_t32 = df_t32.rename({
'Storage \nMedium   ' : 'original_name', 
'Thermal \nconductivity [W/mK]  ': 'kth'
}, axis=1)

df_t32 = df_t32.reset_index(drop=True).set_index('original_name')
df_t32 = df_t32.dropna()

df_t32 = df_t32[['kth']]

df_t32['kth'] = df_t32['kth'].apply(average_range)

df_t32

#%%
df_solid = pd.concat([df_t31,df_t32], axis=1)
df_solid


df_solid = df_solid.astype({
    'T_max': 'pint[degC]',
    'Cp': 'pint[J/kg/K]',
    'mass_density': 'pint[kg/m**3]',
    'specific_price': 'pint[EUR/metric_ton]',
    'kth': 'pint[W/m/K]',
    })

#%%
df_t62 = tables['table_62']
df_t62 = df_t62.dropna(how='all')

df_t62.index.name = 'original_name'

df_t62 = df_t62.rename({
'Melting temperature  [°C] ': 'phase_change_T',
'Heat of fusion  [kJ/kg] ': 'sp_latent_heat',
'Density Solid phase  [kg/m3]': 'mass_density'
}, axis=1)

df_t62 = df_t62[['phase_change_T','sp_latent_heat','mass_density']]

df_t62['phase_change_T'] = df_t62['phase_change_T'].apply(average_range)
df_t62['mass_density'] = df_t62['mass_density'].str.replace('\n','-').apply(average_range)

df_t62 = df_t62.rename({'LiF-CaF2\n80-20%': 'LiF-CaF2'})

df_t62

#%%
df_t63 = tables['table_63']
df_t63 = df_t63.dropna(how='all')

df_t63.index.name = 'original_name'

df_t63 = df_t63.rename({
'Estimated costs PCM  [€/t]': 'specific_price'
}, axis=1)

df_t63 = df_t63[['specific_price']]

df_t63 = df_t63.rename({'KNO3-NaNO2-NaNO3\n53%-41%-6%': 'KNO3-NaNO2-NaNO3'})
df_t63


#%%
df_pcm = pd.concat([df_t62,df_t63], axis=1)
df_pcm

df_pcm = df_pcm.astype({
    'phase_change_T': 'pint[degC]',
    'sp_latent_heat': 'pint[kJ/kg]',
    'mass_density': 'pint[kg/m**3]',
    'specific_price': 'pint[EUR/metric_ton]',
    })

#%%

df_all = pd.concat([df_liquid,df_solid, df_pcm])

df_SM = df_all.drop('specific_price', axis=1)

# The final output deltaT will be calculated with Tmin and Tmax which are averaged between different sources, so these numbers are not quite the same and redundant
df_SM = df_SM.drop('deltaT_max', axis=1)

df_SM.index = df_SM.index.str.replace('[\r\n]+',' ', regex=True) #TODO: Dealing with table extraction newlines in name.. This seems like a robust method of replacing with spaces, should move up and/or implement across all processing scripts. 

df_SM = pd.merge(df_SM, SM_lookup, on='original_name')
df_SM = df_SM.dropna(subset=['SM_name'])
df_SM = df_SM.set_index('SM_name')


df_SM = convert_units(df_SM)
df_SM = prep_df_pint_out(df_SM)

df_SM.to_csv('output/SM_data.csv')

#%%

from es_utils import join_col_vals

df_mat = df_all[['specific_price']]

df_mat = pd.merge(df_mat, mat_lookup, on='original_name')
df_mat = df_mat.dropna(subset=['index'])
df_mat = df_mat.set_index('index')

#Combine the prices of different stone materialsW
specific_prices = df_mat.groupby('index')['specific_price'].mean()
specific_prices.name = 'specific_price'
original_names = df_mat.groupby('index')['original_name'].apply(join_col_vals)
original_names.name = 'original_name'
df_mat = pd.concat([specific_prices,original_names], axis=1)



df_mat = convert_units(df_mat)
df_mat = prep_df_pint_out(df_mat)

df_mat.to_csv('output/mat_data.csv')
