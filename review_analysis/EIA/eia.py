
#%%

import os 
import pandas as pd
import matplotlib.pyplot as plt


input_folder = r'input_data\eia8602021'

# %%


fp = os.path.join(input_folder, '3_4_Energy_Storage_Y2021.xlsx')
df_storage = pd.read_excel(fp, skiprows=1, 
                           dtype={
    'Technology': str
}
)

df_storage.info()

#%%
import numpy as np

df_storage['Nameplate Energy Capacity (MWh)'] =  df_storage['Nameplate Energy Capacity (MWh)'].astype(str).str.replace(' ', 'nan').astype(float)

df_storage['Technology'] = df_storage['Technology'].str.replace(
'Solar Thermal with Energy Storage', 'CSP').str.replace(
'Natural Gas with Compressed Air Storage', 'CAES (Nat gas)'
)

#%%

df_storage['Technology'].value_counts()

#%%

df_bat = df_storage.where(df_storage['Technology'] == 'Batteries').dropna(how='all')

df_bat['Storage Technology 1'].value_counts().plot.bar()



#%%

pow_caps = df_storage.groupby('Technology')['Nameplate Capacity (MW)'].sum()
pow_caps = pow_caps.sort_values(ascending=False)
pow_caps.plot.bar()

plt.ylabel("Cumulative Power Capacity (MW)")
plt.yscale('log')

plt.tight_layout()
plt.savefig('figures/3_4_storage_cap_MW.png')

#%%

e_caps = df_storage.groupby('Technology')['Nameplate Energy Capacity (MWh)'].sum()
e_caps = e_caps.sort_values(ascending=False)
e_caps.plot.bar()

plt.ylabel("Cumulative Energy Capacity (MWh)")
plt.yscale('log')

plt.tight_layout()
plt.savefig('figures/3_4_storage_cap_MWh.png')

#%%

df_storage['duration'] = df_storage['Nameplate Energy Capacity (MWh)']/df_storage['Nameplate Capacity (MW)']

df_storage.groupby('Technology')['duration'].hist()

plt.ylabel('Count')
plt.xlabel('duration')


#%%

import seaborn as sns

bins = [0,0.3,1,3,10]

df_storage['dur_bin'] = pd.cut(df_storage['duration'], bins = bins)

df_stats = df_storage.groupby(['dur_bin', 'Technology'])['Nameplate Energy Capacity (MWh)'].sum()
df_stats = df_stats.reset_index()

df_stats

# df_statsdf_stats.reset_index('mid_type_2')

plt.figure()
sns.barplot(data=df_stats, x='dur_bin', y='Nameplate Energy Capacity (MWh)', hue='Technology')
plt.yscale('log')
plt.xticks(rotation = 90)
# plt.gca().get_legend().set_bbox_to_anchor([0,0,1.6,1])
plt.ylabel('Energy Capacity in \nDuration Range (kWh)')
plt.xlabel('Duration Range (hours)')


#%%

fp = os.path.join(input_folder, '3_1_Generator_Y2021.xlsx')
df_gen = pd.read_excel(fp, skiprows=1)

df_gen.info()


#%%

df_gen['Nameplate Capacity (MW)'].sum()

#%%



df_gen['Technology'].value_counts()

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
'Natural Gas with Compressed Air Storage', 'CAES (Nat gas)').str.replace(
'Hydroelectric Pumped Storage', 'PHES'
)

# %%
df_gen_s.info()

#%%

pow_caps = df_gen_s.groupby('Technology')['Nameplate Capacity (MW)'].sum()

# plt.ylabel("Cumulative Power Capacity")
pow_caps = pow_caps.sort_values(ascending=False)
pow_caps.plot.bar()

plt.ylabel("Cumulative Power Capacity (MW)")
plt.yscale('log')

plt.tight_layout()
plt.savefig('figures/gen_cap_MW.png')


#%%

df_gen_hydro = df_gen.where(df_gen['Technology'].isin([
    'Hydroelectric Pumped Storage',
])).dropna(how='all').dropna(how='all', axis=1)

# %%
# df_gen_hydro.to_csv('hydro.csv')

#%%

# df_gen_hydro['Plant Name'].drop_duplicates().to_csv('hydro_lookup.csv')
# df_gen_hydro[['Plant Name','Plant Code']].drop_duplicates(subset='Plant Name').to_csv('hydro_lookup_2.csv')


#%%
import json



gesdb_folder = r'C:\Users\aspit\Git\Energy-Storage-Analysis\LDES-Viability\GESDB'


fp = os.path.join(gesdb_folder, 'data/GESDB_Project_Data.json')

with open(fp, 'r', encoding='utf-8') as f:
    data = json.load(f)

df = pd.DataFrame.from_dict(data)

df = df.set_index('ID')

df['Subsystems'] = df['Subsystems'].apply(lambda x: x[0])


df = df[['Data Source','Project/Plant Name', 'Status', 'Rated Power (kW)', 'Discharge Duration at Rated Power (hrs)', 'Storage Capacity (kWh)', 'Subsystems']]


df = df.rename({
'Data Source': 'source',
'Project/Plant Name': 'name',
'Status': 'status', 
'Rated Power (kW)': 'power', 
'Discharge Duration at Rated Power (hrs)': 'duration', 
'Storage Capacity (kWh)': 'energy',
'Subsystems': 'subsystems'
}, axis=1)

# %%
# df.loc[hydro_lookup]

hydro_lookup = pd.read_csv('hydro_lookup.csv', index_col=0)
hydro_lookup = hydro_lookup.dropna(subset=['GESDB_ID'])

df_hydro_gesdb = df.loc[hydro_lookup['GESDB_ID']]

df_hydro_gesdb['Plant Code'] = hydro_lookup['Plant Code'].values

# df_hydro_gesdb.set_index('P')

df_hydro_gesdb = df_hydro_gesdb[['Plant Code', 'name', 'energy','power','duration']]
df_hydro_gesdb['energy'] = df_hydro_gesdb['energy']/1000 
df_hydro_gesdb['power'] = df_hydro_gesdb['power']/1000 

df_hydro_gesdb
# %%


nameplate_sum = df_gen_hydro.groupby('Plant Code')[['Nameplate Capacity (MW)']].sum()
first_name = df_gen_hydro.groupby('Plant Code')[['Plant Name']].first()

eia_hydro = pd.concat([nameplate_sum, first_name], axis=1)

df_together = pd.merge(eia_hydro, df_hydro_gesdb, on='Plant Code')

df_together

# %%
df_together['ratio'] = df_together['power']/df_together['Nameplate Capacity (MW)']

df_together['ratio']
# %%

df_together['ratio'].hist()


#%%

df_together['energy']