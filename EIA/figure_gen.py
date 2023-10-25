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

palette = sns.color_palette("tab10")
palette


powcap_gen = df_gen.groupby('Technology')['Nameplate Capacity (MW)'].sum()
pow_caps = powcap_gen.sort_values(ascending=False)
pow_caps = pow_caps.drop('CSP')

#%%

import numpy as np

df_lib = df_storage.where(df_storage['sub_type'] == 'LIB').dropna(how='all')

bins = np.logspace(np.log10(0.2),np.log10(10), 20)
# bins

df_lib['duration'].hist(bins=bins)

plt.xscale('log')

plt.ylabel("Count")
plt.xlabel("Duration [h]")

#%%

# colors = ['red','green','blue','purple']

colors = {
    'Batteries': palette[0],
    'CAES': palette[1],
    'Flywheels':palette[2],
    'PHES':palette[3]
}

ax = sns.barplot(x=pow_caps.index, y=pow_caps.values, palette=colors)

# pow_caps.plot.bar(color=colors)

plt.ylabel("Cumulative Power Capacity (MW)")
plt.yscale('log')


# plt.legend(ax.lines, labels=colors.keys())

plt.tight_layout()
# sns.bar``


plt.savefig('figures/eia_cap_MW.png')

#%%

#%%

powcap_store = df_storage.groupby('type')['power'].sum()

# print("Generator Dataset")
# print(powcap_gen)
# print("Storage Dataset")
# print(powcap_store)

#%%


df_storage['duration'].hist()

plt.ylabel('Count')
plt.xlabel('duration')

#%%

bins = [0,0.3,1,3,10,30,100]

df_storage['dur_bin'] = pd.cut(df_storage['duration'], bins = bins)

df_stats = df_storage.groupby(['dur_bin', 'type'])['energy'].sum()
df_stats = df_stats.reset_index()

plt.figure(figsize=(2.3, 2.5))
ax = sns.barplot(data=df_stats, x='dur_bin', y='energy', hue='type', palette=colors)
plt.yscale('log')
plt.xticks(rotation = 90)

plt.ylim(1e0,1e6)

# plt.gca().get_legend().set_bbox_to_anchor([0,0,1.6,1])
plt.ylabel('Energy Capacity in \nDuration Range (MWh)')
plt.xlabel('Duration Range (hours)')

ax.get_legend().remove()
# plt.legend()


plt.tight_layout()
plt.savefig('figures/duration_bins.png')

#%%


plt.figure()
ax = sns.barplot(data=df_stats, x='dur_bin', y='energy', hue='type', palette=colors)
plt.legend()
plt.savefig('figures/duration_bins_legend.png')


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


df_no_bat = df_storage.where(df_storage['type'] != 'Batteries').dropna(how='all')
df_no_bat = df_no_bat.groupby('type')[['energy','power']].sum()
# p_caps_no_bat = df_no_bat.groupby('type')['power'].sum()

df_bat = df_storage.where(df_storage['type'] == 'Batteries').dropna(how='all')

df_bat['sub_type'] = df_bat['sub_type'].map(bat_map)


df_bat = df_bat.groupby('sub_type')[['energy','power']].sum()



# p_caps_bat = df_bat.groupby('type')['power'].sum()

df_all = pd.concat([df_no_bat, df_bat])


#%%


colors = {
    'CAES': palette[1],
    'Flywheels':palette[2],
    'PHES':palette[3]
}

colors.update({name: palette[0] for name in bat_map.values()})


e_caps_all = df_all['energy'].sort_values(ascending=False)


ax = sns.barplot(x=e_caps_all.index, y=e_caps_all.values, palette=colors)

plt.ylabel("Cumulative Energy Capacity (MWh)")
plt.yscale('log')
plt.xlabel("Battery Type")

plt.xlabel("Technology")

plt.xticks(rotation = 90)

plt.tight_layout()

plt.savefig('figures/e_cap_all.png')

#%%

data = df_all.reset_index().sort_values('energy', ascending=False)

x_ = 'index' 
y_ = 'energy'
y_2 = 'power'

data1 = data[[x_, y_]]
data2 = data[[x_, y_2]]
plt.figure(figsize=(2.5, 2.6))
ax = sns.barplot(x=x_, y=y_, data=data1, palette=colors)
width_scale = 0.45
for bar in ax.containers[0]:
    bar.set_width(bar.get_width() * width_scale)
# ax.yaxis.set_major_formatter(PercentFormatter(1))


plt.xticks(rotation = 90)

ax2 = ax.twinx()
sns.barplot(x=x_, y=y_2, data=data2, alpha=1, hatch='///', ax=ax2, palette=colors)
for bar in ax2.containers[0]:
    x = bar.get_x()
    w = bar.get_width()
    bar.set_x(x + w * (1- width_scale))
    bar.set_width(w * width_scale)


ax.set_yscale('log')
ax.set_ylim(1,1e6)
# ax.set


ax.set_ylabel('Cumulative Energy Capacity (MWh)')
ax.set_xlabel("Technology")

ax2.set_yscale('log')
ax2.set_ylim(1,1e6)

ax2.set_ylabel('Cumulative Power Capacity (MW)')
# plt.legend()
plt.tight_layout()

plt.savefig('figures/energy_and_power.png')
# plt.show()
# %%
