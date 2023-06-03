#%%

import os 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

input_folder = r'input_data'

df_storage = pd.read_csv('input_data/storage_processed.csv', index_col=0)
df_gen = pd.read_csv('input_data/gen_processed.csv', index_col=0)

fp_gesdb = os.path.join(REPO_DIR, 'GESDB', 'data', 'gesdb_processed.csv')
df_gesdb = pd.read_csv(fp_gesdb, index_col=0)
df_gesdb = df_gesdb.drop('subsystems', axis=1)
df_gesdb

# %%

hydro_lookup = pd.read_csv('hydro_lookup.csv', index_col=0)
hydro_lookup = hydro_lookup.dropna(subset=['GESDB_ID'])

df_hydro_gesdb = df_gesdb.loc[hydro_lookup['GESDB_ID']]

df_hydro_gesdb['Plant Code'] = hydro_lookup['Plant Code'].values

df_hydro_gesdb = df_hydro_gesdb[['Plant Code', 'name', 'energy','power','duration']]
df_hydro_gesdb['energy'] = df_hydro_gesdb['energy']/1000 
df_hydro_gesdb['power'] = df_hydro_gesdb['power']/1000 

df_hydro_gesdb

#%%


df_gen_hydro = df_gen.where(df_gen['Technology'].isin([
    'PHES',
])).dropna(how='all').dropna(how='all', axis=1)

nameplate_sum = df_gen_hydro.groupby('Plant Code')[['Nameplate Capacity (MW)']].sum()
first_name = df_gen_hydro.groupby('Plant Code')[['Plant Name']].first()

eia_hydro = pd.concat([nameplate_sum, first_name], axis=1)

df_together = pd.merge(eia_hydro, df_hydro_gesdb, on='Plant Code')
df_together['ratio'] = df_together['power']/df_together['Nameplate Capacity (MW)']

df_together

#%%

pow_caps = df_gen.groupby('Technology')['Nameplate Capacity (MW)'].sum()

# plt.ylabel("Cumulative Power Capacity")
pow_caps = pow_caps.sort_values(ascending=False)
pow_caps.plot.bar()

plt.ylabel("Cumulative Power Capacity (MW)")
plt.yscale('log')

plt.tight_layout()
plt.savefig('figures/gen_cap_MW.png')

#%%

pow_caps = df_storage.groupby('Technology')['Nameplate Capacity (MW)'].sum()
pow_caps = pow_caps.sort_values(ascending=False)
pow_caps.plot.bar()

plt.ylabel("Cumulative Power Capacity (MW)")
plt.yscale('log')

plt.tight_layout()
plt.savefig('figures/3_4_storage_cap_MW.png')
#%%

df_storage['duration'] = df_storage['Nameplate Energy Capacity (MWh)']/df_storage['Nameplate Capacity (MW)']

df_storage['duration'].hist()

plt.ylabel('Count')
plt.xlabel('duration')

#%%

bins = [0,0.3,1,3,10]

df_storage['dur_bin'] = pd.cut(df_storage['duration'], bins = bins)

df_stats = df_storage.groupby(['dur_bin', 'Technology'])['Nameplate Energy Capacity (MWh)'].sum()
df_stats = df_stats.reset_index()

plt.figure()
sns.barplot(data=df_stats, x='dur_bin', y='Nameplate Energy Capacity (MWh)', hue='Technology')
plt.yscale('log')
plt.xticks(rotation = 90)
# plt.gca().get_legend().set_bbox_to_anchor([0,0,1.6,1])
plt.ylabel('Energy Capacity in \nDuration Range (kWh)')
plt.xlabel('Duration Range (hours)')

#%%

e_caps = df_storage.groupby('Technology')['Nameplate Energy Capacity (MWh)'].sum()
e_caps = e_caps.sort_values(ascending=False)
e_caps.plot.bar()

plt.ylabel("Cumulative Energy Capacity (MWh)")
plt.yscale('log')

plt.tight_layout()
plt.savefig('figures/3_4_storage_cap_MWh.png')

#%%

df_bat = df_storage.where(df_storage['Technology'] == 'Batteries').dropna(how='all')

df_bat['Storage Technology 1'].value_counts().plot.bar()
