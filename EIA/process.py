
import os 
import pandas as pd
import matplotlib.pyplot as plt

from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

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

if not os.path.exists('processed_data'): os.mkdir('processed_data')

df_gen_s.to_csv('processed_data/df_gen.csv')


#%%

# Generate lookup table for pumped hydro

# df_gen_hydro = df_gen.where(df_gen['Technology'].isin([
#     'Hydroelectric Pumped Storage',
# ])).dropna(how='all').dropna(how='all', axis=1)

# df_gen_hydro.to_csv('hydro.csv')

# df_gen_hydro['Plant Name'].drop_duplicates().to_csv('hydro_lookup.csv')
# df_gen_hydro[['Plant Name','Plant Code']].drop_duplicates(subset='Plant Name').to_csv('hydro_lookup_2.csv')


#%%


df_gen = df_gen_s


import numpy as np
def assert_same_str(l):
    l = [s for s in l if str(s) != 'nan']
    s = list(set(l))
    if len(s) > 1:
        print(s)
        raise ValueError
    elif len(s) == 0:
        return np.nan
    else:
        return s[0]

#%%

df_eia_store = df_storage[['Plant Name','Technology', 'Nameplate Capacity (MW)', 'Status', 'Storage Technology 1', 'Nameplate Energy Capacity (MWh)']]

df_eia_store = df_eia_store.where(df_eia_store['Status'] == 'OP').drop('Status', axis=1).dropna(how='all')

df_eia_store = df_eia_store.rename({
'Plant Name': 'name',
'Technology': 'type',
'Nameplate Capacity (MW)': 'power',
'Storage Technology 1': 'sub_type',
'Nameplate Energy Capacity (MWh)': 'energy'
}, axis=1)

# df_eia_store['name'] = df_eia_store['energy']/df_eia_store['power']

# Here we group by each plant code, as there are multiple generators per plant.
# All string values should be the same and energy and power capacities are
# summed. 

df_eia_store = pd.concat([
df_eia_store.groupby('Plant Code')['name'].apply(assert_same_str),
df_eia_store.groupby('Plant Code')['type'].apply(assert_same_str),
df_eia_store.groupby('Plant Code')['sub_type'].apply(assert_same_str),
df_eia_store.groupby('Plant Code')['energy'].sum(),
df_eia_store.groupby('Plant Code')['power'].sum(),
], axis=1)


#%%

df_eia_gen = df_gen[['Plant Name', 'Technology', 'Nameplate Capacity (MW)', 'Status']]
df_eia_gen = df_eia_gen.where(df_eia_gen['Status'] == 'OP').drop('Status', axis=1)

df_eia_gen = df_eia_gen.rename({
'Plant Name': 'name',
'Technology': 'type',
'Nameplate Capacity (MW)': 'power',
}, axis=1)

df_eia_hydro = df_eia_gen.where(df_eia_gen['type'] == 'PHES').dropna(how='all')


df_eia_hydro = pd.concat([
df_eia_hydro.groupby('Plant Code')['name'].apply(assert_same_str),
df_eia_hydro.groupby('Plant Code')['type'].apply(assert_same_str),
df_eia_hydro.groupby('Plant Code')['power'].sum(),
], axis=1)


df_eia_hydro


#%%

fp_gesdb = os.path.join(REPO_DIR, 'GESDB', 'data', 'gesdb_processed.csv')
df_gesdb = pd.read_csv(fp_gesdb, index_col=0)
df_gesdb = df_gesdb.drop('subsystems', axis=1).drop('broad_category', axis=1)

df_gesdb
df_gesdb['energy'] = df_gesdb['energy']/1000 
df_gesdb['power'] = df_gesdb['power']/1000 

df_gesdb

# %%

hydro_lookup = pd.read_csv('hydro_lookup.csv', index_col=0)
hydro_lookup = hydro_lookup.dropna(subset=['GESDB_ID'])

df_hydro_gesdb = df_gesdb.loc[hydro_lookup['GESDB_ID']]

df_hydro_gesdb['Plant Code'] = hydro_lookup['Plant Code'].values

df_hydro_gesdb = df_hydro_gesdb[['Plant Code', 'status','name', 'energy','power','duration']]

# print("Length all hydro: {}".format(len(df_hydro_gesdb)))
df_hydro_gesdb = df_hydro_gesdb.where(df_hydro_gesdb['status'] == 'Operational').dropna(how='all').drop('status', axis=1)
# print("Length operational hydro: {}".format(len(df_hydro_gesdb)))

df_hydro_gesdb = df_hydro_gesdb.rename({
    col: '{}_gesdb'.format(col) for col in df_hydro_gesdb.columns if col != 'Plant Code'
}, axis=1)

df_hydro_gesdb.head()

#%%

df_hydro = pd.merge(df_eia_hydro, df_hydro_gesdb, on='Plant Code').set_index('Plant Code')


# print("{} out of {} PHES have 0 duration, dropping. ".format(
# df_hydro['duration_gesdb'].value_counts().sort_index()[0],
# df_hydro['duration_gesdb'].value_counts().sort_index().sum()
# ))


df_hydro = df_hydro.where(df_hydro['duration_gesdb'] > 0).dropna(how='all')

df_hydro

#%%
power_ratio = df_hydro['power_gesdb']/df_hydro['power']

power_ratio.hist()

plt.xlabel("GESDB/EIA Power Ratio")

#%%

df_hydro['energy'] = df_hydro['power']*df_hydro['duration_gesdb']



df_hydro_final = df_hydro.drop(['name_gesdb', 'energy_gesdb','power_gesdb'], axis=1)
df_hydro_final = df_hydro_final.rename({'duration_gesdb':'duration'},axis=1)


#%%

df_hydro_final

#%%

df_eia_store.loc[7063,'energy'] = df_gesdb.loc[189,'energy']
df_eia_store['duration'] = df_eia_store['energy']/df_eia_store['power']

# df_eia_store.where(df_eia_store['type']=='CAES').dropna(how='all')



#%%

df_storage = pd.concat([df_eia_store, df_hydro_final])

df_storage = df_storage.where(df_storage['type'] != 'CSP').dropna(how='all')

df_storage.to_csv('processed_data/df_storage.csv')
