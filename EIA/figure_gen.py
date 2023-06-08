#%%

import os 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

if not os.path.exists('figures'): os.mkdir('figures')
import matplotlib as mpl
mpl.rcParams.update({'font.size': 7, 'savefig.dpi': 600, 'font.sans-serif': 'arial', 'figure.figsize': (2.3, 2.5)})

# import seaborn as sns
# sns.set_theme()

from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

input_folder = r'input_data'

df_gen = pd.read_csv('processed_data/df_gen.csv', index_col=0)
df_storage = pd.read_csv('processed_data/df_storage.csv', index_col=0)


#%%



#%%

powcap_gen = df_gen.groupby('Technology')['Nameplate Capacity (MW)'].sum()
pow_caps = powcap_gen.sort_values(ascending=False)
pow_caps = pow_caps.drop('CSP')

pow_caps.plot.bar()

plt.ylabel("Cumulative Power Capacity (MW)")
plt.yscale('log')

plt.tight_layout()
plt.savefig('figures/eia_cap_MW.png')

#%%

colors = ['red','green','blue','purple']

sns.barplot(x=pow_caps.index, y=pow_caps.values, palette=colors)

plt.ylabel("Cumulative Power Capacity (MW)")
plt.yscale('log')

plt.tight_layout()
# sns.bar``


#%%

#%%

powcap_store = df_storage.groupby('type')['power'].sum()

print("Generator Dataset")
print(powcap_gen)
print("Storage Dataset")
print(powcap_store)

#%%


df_storage['duration'].hist()

plt.ylabel('Count')
plt.xlabel('duration')

#%%

bins = [0,0.3,1,3,10,30,100]

df_storage['dur_bin'] = pd.cut(df_storage['duration'], bins = bins)

df_stats = df_storage.groupby(['dur_bin', 'type'])['energy'].sum()
df_stats = df_stats.reset_index()

plt.figure()
sns.barplot(data=df_stats, x='dur_bin', y='energy', hue='type')
plt.yscale('log')
plt.xticks(rotation = 90)

plt.ylim(5e0,2e6)

# plt.gca().get_legend().set_bbox_to_anchor([0,0,1.6,1])
plt.ylabel('Energy Capacity in \nDuration Range (MWh)')
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

plt.xlabel("Technology")

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
plt.xlabel("Battery Type")

plt.tight_layout()
plt.savefig("figures/batt_type.png")

# %%
