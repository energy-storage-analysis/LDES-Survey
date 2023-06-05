
import os 
import pandas as pd
import matplotlib.pyplot as plt


input_folder = r'input_data\eia8602021'

fp = os.path.join(input_folder, '3_4_Energy_Storage_Y2021.xlsx')
df_storage = pd.read_excel(fp, skiprows=1, 
                           dtype={
    'Technology': str
}, index_col=0
)

df_storage['Nameplate Energy Capacity (MWh)'] =  df_storage['Nameplate Energy Capacity (MWh)'].astype(str).str.replace(' ', 'nan').astype(float)

df_storage['Technology'] = df_storage['Technology'].str.replace(
'Solar Thermal with Energy Storage', 'CSP').str.replace(
'Natural Gas with Compressed Air Storage', 'CAES'
)
df_storage = df_storage.set_index('Plant Code')

df_storage.to_csv('input_data/storage_processed.csv')

#%%

fp = os.path.join(input_folder, '3_1_Generator_Y2021.xlsx')
df_gen = pd.read_excel(fp, skiprows=1, index_col=0)

df_gen.info()


#%%

df_gen_s = df_gen.where(df_gen['Technology'].isin([
    'Batteries',
    'Hydroelectric Pumped Storage',
    'Flywheels',
    'Natural Gas with Compressed Air Storage',
    'Solar Thermal with Energy Storage'
])).dropna(how='all').dropna(how='all', axis=1)


df_gen_s['Technology'] = df_gen_s['Technology'].str.replace(
'Solar Thermal with Energy Storage', 'CSP').str.replace(
'Natural Gas with Compressed Air Storage', 'CAES').str.replace(
'Hydroelectric Pumped Storage', 'PHES'
)

df_gen_s = df_gen_s.set_index('Plant Code')

df_gen_s.to_csv('input_data/gen_processed.csv')


#%%

# Generate lookup table for pumped hydro

# df_gen_hydro = df_gen.where(df_gen['Technology'].isin([
#     'Hydroelectric Pumped Storage',
# ])).dropna(how='all').dropna(how='all', axis=1)

# df_gen_hydro.to_csv('hydro.csv')

# df_gen_hydro['Plant Name'].drop_duplicates().to_csv('hydro_lookup.csv')
# df_gen_hydro[['Plant Name','Plant Code']].drop_duplicates(subset='Plant Name').to_csv('hydro_lookup_2.csv')
