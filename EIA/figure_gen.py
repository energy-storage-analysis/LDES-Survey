#%%

import os 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

if not os.path.exists('figures'): os.mkdir('figures')
import matplotlib as mpl
mpl.rcParams.update({'font.size': 7, 'savefig.dpi': 600, 'font.sans-serif': 'arial', 'figure.figsize': (2.3, 2.5)})

from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

input_folder = r'input_data'

df_storage = pd.read_csv('input_data/storage_processed.csv', index_col=0)
df_gen = pd.read_csv('input_data/gen_processed.csv', index_col=0)

#%%


#%%

powcap_gen = df_gen.groupby('Technology')['Nameplate Capacity (MW)'].sum()
powcap_store = df_storage.groupby('Technology')['Nameplate Capacity (MW)'].sum()

print("Generator Dataset")
print(powcap_gen)
print("Storage Dataset")
print(powcap_store)

#%%

# plt.ylabel("Cumulative Power Capacity")
pow_caps = powcap_gen.sort_values(ascending=False)
pow_caps.plot.bar()

plt.ylabel("Cumulative Power Capacity (MW)")
plt.yscale('log')

plt.tight_layout()
plt.savefig('figures/eia_cap_MW.png')


#%%

df_storage.info()

#%%

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

print("Length all hydro: {}".format(len(df_hydro_gesdb)))
df_hydro_gesdb = df_hydro_gesdb.where(df_hydro_gesdb['status'] == 'Operational').dropna(how='all').drop('status', axis=1)
print("Length operational hydro: {}".format(len(df_hydro_gesdb)))

df_hydro_gesdb = df_hydro_gesdb.rename({
    col: '{}_gesdb'.format(col) for col in df_hydro_gesdb.columns if col != 'Plant Code'
}, axis=1)

df_hydro_gesdb.head()

#%%

df_hydro = pd.merge(df_eia_hydro, df_hydro_gesdb, on='Plant Code').set_index('Plant Code')


print("{} out of {} PHES have 0 duration, dropping. ".format(
df_hydro['duration_gesdb'].value_counts().sort_index()[0],
df_hydro['duration_gesdb'].value_counts().sort_index().sum()
))


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

df_hydro_final.info()

#%%

df_hydro_final

#%%

df_eia_store.loc[7063,'energy'] = df_gesdb.loc[189,'energy']
df_eia_store['duration'] = df_eia_store['energy']/df_eia_store['power']

# df_eia_store.where(df_eia_store['type']=='CAES').dropna(how='all')



#%%

df_storage = pd.concat([df_eia_store, df_hydro_final])

df_storage = df_storage.where(df_storage['type'] != 'CSP').dropna(how='all')

df_storage


#%%


df_storage['duration'].hist()

plt.ylabel('Count')
plt.xlabel('duration')

#%%

bins = [0,1,10,100]

df_storage['dur_bin'] = pd.cut(df_storage['duration'], bins = bins)

df_stats = df_storage.groupby(['dur_bin', 'type'])['energy'].sum()
df_stats = df_stats.reset_index()

plt.figure()
sns.barplot(data=df_stats, x='dur_bin', y='energy', hue='type')
plt.yscale('log')
plt.xticks(rotation = 90)

plt.ylim(5e0,2e6)

# plt.gca().get_legend().set_bbox_to_anchor([0,0,1.6,1])
plt.ylabel('Energy Capacity in \nDuration Range (kWh)')
plt.xlabel('Duration Range (hours)')

plt.legend()

plt.tight_layout()
plt.savefig('figures/duration_bins.png')

#%%

plt.figure()

e_caps = df_storage.groupby('type')['energy'].sum()
e_caps = e_caps.sort_values(ascending=False)
e_caps.plot.bar()

plt.ylabel("Cumulative Energy Capacity (MWh)")
plt.yscale('log')

plt.tight_layout()
plt.savefig('figures/storage_cap_MWh.png')

#%%

plt.figure()

df_bat = df_storage.where(df_storage['type'] == 'Batteries').dropna(how='all')


bat_map = {
    'LIB': 'Li-Ion',
    'PBB': 'Lead Acid',
    'OTH': 'Other',
    'NIB': 'Nickel-Based',
    'FLB': 'Flow',
    'NAB': 'Sodium-Based'
}

df_bat['sub_type'] = df_bat['sub_type'].map(bat_map)

# df_bat['sub_type'].value_counts().plot.bar()

e_caps = df_bat.groupby('sub_type')['energy'].sum()

e_caps = e_caps.sort_values(ascending=False)
e_caps.plot.bar()

plt.ylabel("Cumulative Energy Capacity (MWh)")
plt.yscale('log')

plt.tight_layout()
plt.savefig("figures/batt_type.png")
