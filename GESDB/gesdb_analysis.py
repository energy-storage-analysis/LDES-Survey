#%%
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import pandas as pd 
import json

mpl.rcParams.update({'font.size': 12, 'savefig.dpi': 600, 'font.sans-serif': 'arial', 'figure.figsize': (7, 5)})

# %%

fp = 'data/GESDB_Project_Data.json'

with open(fp, 'r', encoding='utf-8') as f:
    data = json.load(f)

df = pd.DataFrame.from_dict(data)
df = df.set_index('ID')
#%%
# df['Subsystems'].apply(len).value_counts()
#There are only single subsystems...just pull out first (and only) element
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
df 


df.info()
# %%

df_sd = df['subsystems'].apply(pd.Series)['Storage Device'].apply(pd.Series)

df_sd = df_sd[['Technology Broad Category',  'Technology Mid-Type', 'Technology Sub-Type']]

df_sd = df_sd.rename({
'Technology Broad Category': 'broad_category',  
'Technology Mid-Type': 'mid_type', 
'Technology Sub-Type': 'sub_type'
}, axis=1)

df_sd


#%%

df2 = pd.merge(df, df_sd, on='ID')
df2 = df2[df2['energy'] > 0]
df2 = df2[df2['status'] == 'Operational']

#There is one Hydro plant with this duration...Seems to be a big lake
#https://sandia.gov/ess-ssl/gesdb/public/projects.html#32
# df2 = df2[df2['duration'] <10000]

df2 = df2[df2['mid_type'] != '']

df2['mid_type'].value_counts().index

cat_map = {
'Lithium-ion battery': 'Lithium-ion', 
'Pumped hydro storage': 'Pumped Hydro', 
'Compressed air energy storage': 'CAES', 
'Sensible heat': 'Thermal',
'Latent heat': 'Thermal', 
'Lead-acid battery':'Lead-acid',
# 'Flow battery', 
'Sodium-based battery':'Sodium-based' ,
'Heat thermal storage': 'Thermal', 
# 'Flywheel',
'Electro-chemical capacitor': 'Pseudocapacitor',
'Nickel-based battery': 'Nickel-based', 
'Hydrogen storage': 'Hydrogen'
    }

# df2 = 

df2['mid_type'] = [cat_map[s] if s in cat_map else s for s in df2['mid_type']]

#Get rid of thermal. Checked manually and all are CSP plants, or low temperature. 
# TODO: this is true except for one LAES pilot, perhaps should include that, but its small capacity.
df2 = df2[df2['mid_type'] != 'Thermal']

#%%

df2['broad_category'].value_counts()
# %%
df2['mid_type'].value_counts()

# %%


energy_total = df2.groupby('mid_type')['energy'].sum().sort_values(ascending=False)
power_total = df2.groupby('mid_type')['power'].sum().sort_values(ascending=False)

plt.figure()
energy_total.plot.bar()
plt.yscale('log')
plt.ylabel('Total Energy \nCapacity (kWh)')
plt.xlabel('Technology')
plt.tight_layout()
# plt.xticks(rotation=60)

plt.savefig('output/energy_cap_tech.png', dpi=600)

# %%

power_total.plot.bar()
plt.yscale('log')
# %%

bins = np.logspace(np.log10(0.1), np.log10(2000), 20)

# df2['duration'].hist(bins=bins)

sns.histplot(data=df2, x='duration', hue='broad_category', bins=bins)

plt.xscale('log')
plt.ylabel('Count')
plt.xlabel('Nominal Discharge Duration (hours)')
# %%


sns.histplot(data=df2, x='duration', weights=df2['energy'], hue='broad_category', bins=bins)

plt.xscale('log')
plt.yscale('log')
plt.ylabel('Binned Energy Capacity (kWh)')

plt.ylim(1e3,1e11)

#%%

cat_keep = ['Pumped Hydro','CAES','Lithium-ion','Thermal']

df2['mid_type_2'] = [s if s in cat_keep else 'Other' for s in df2['mid_type']]

sns.histplot(data=df2, x='duration', weights=df2['energy'], hue='mid_type_2', bins=bins)
plt.xscale('log')
plt.yscale('log')

plt.gca().get_legend().set_bbox_to_anchor([0,0,1.6,1])
# %%

bins = [0.3,1,3,10,30,100,300]
# bins=[0.3,3,30,300]
# bins = np.logspace(np.log10(0.1), np.log10(1000), 5)

df2['dur_bin'] = pd.cut(df2['duration'], bins = bins)
# energy_bins = df2.groupby('dur_bin')['energy'].sum()


sns.barplot(data=df2, x='dur_bin', y='energy', hue='mid_type_2')

plt.yscale('log')


#%%

df_stats = df2.groupby(['dur_bin', 'mid_type_2']).sum()


df_stats = df_stats.reset_index()




df_stats

# df_statsdf_stats.reset_index('mid_type_2')

plt.figure()
sns.barplot(data=df_stats, x='dur_bin', y='energy', hue='mid_type_2')
plt.yscale('log')
plt.xticks(rotation = 45)
# plt.gca().get_legend().set_bbox_to_anchor([0,0,1.6,1])
plt.ylabel('Cumulative Energy Capacity in \nDuration Range (kWh)')
plt.xlabel('Duration Range (hours)')

# plt.ylim(1e3,1e11)

plt.legend()
plt.tight_layout()

plt.savefig('output/energy_vs_duration.png', dpi=600)

# %%



# df2[df2['broad_category'] == 'Thermal energy storage']

# df2['broad_category'].value_counts()
# %%


df2[df2['mid_type'] == 'Sodium-based'].sort_values('energy', ascending=False)
# df2['mid_type_2'].value_counts()
#%%
df2[df2['mid_type'] == 'Lithium-ion'].sort_values('duration', ascending=False)


#%%
therm = df2[df2['mid_type'] == 'Thermal'].sort_values('energy', ascending=False)

therm['sub_type'].value_counts()
# therm[therm['sub_type'] == 'Liquid air energy storage']
# therm[therm['sub_type'] == 'Concrete blocks, rocks, and sand-like particles']



# %%
