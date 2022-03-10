#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df_prices = pd.read_csv('data/df_prices.csv', index_col=0)
df_all = pd.read_csv('data/combined_all.csv', index_col=0)

#%%

df_sp_energy = df_all.dropna(subset=['specific_energy'])

df_sp_energy = df_sp_energy[['energy_type','specific_energy', 'index_name']]

#TODO: improve handling
df_sp_energy = df_sp_energy.where(df_sp_energy['index_name'] != 'O3U').dropna(how='all')

df_sp_energy.info()

#%%k

present_prices = [n for n in df_sp_energy['index_name'] if n in df_prices.index]
missing_prices = [n for n in df_sp_energy['index_name'] if n not in df_prices.index]

if len(missing_prices):
    print("Did not find any price (including elemental) for the following")
    print(missing_prices)
    print("dropping from energy dataset")


df_sp_energy = df_sp_energy.where(df_sp_energy['index_name'].isin(present_prices)).dropna(how='all')
df_sp_energy.info()
# %%
df_prices['specific_price_avg'] = sum([
    df_prices['specific_price_refs'].fillna(0),
    df_prices['specific_price_element'].fillna(0)
])/2


df_prices


#%%
# %%

df_vis = df_sp_energy[['index_name', 'energy_type', 'specific_energy']]



df_vis['specific_price_avg'] = df_prices['specific_price_avg'].loc[df_sp_energy['index_name']].values

df_vis['C_kwh'] = df_vis['specific_price_avg']/df_vis['specific_energy']

df_vis

#%%

df_li_ec = pd.read_csv(r'C:\Users\aspit\Git\MHDLab-Projects\Energy Storage Analysis\datasets\pdf\li_2017\output\process_couples.csv')

df_li_ec = df_li_ec[['label','C_kwh','C_kwh_orig','specific_price','specific_energy']]

df_li_ec = df_li_ec.rename({'label':'index_name'}, axis=1)

df_li_ec_calc = df_li_ec[['index_name', 'C_kwh']] 
df_li_ec_calc['energy_type'] = 'EC Couples (Li 2017 Calc)'
df_li_ec_orig = df_li_ec[['index_name', 'C_kwh_orig']].rename({'C_kwh_orig': 'C_kwh'},axis=1)
df_li_ec_orig['energy_type'] = 'EC Couples (Li 2017 Orig)'


df_vis = pd.concat([df_vis, df_li_ec_calc, df_li_ec_orig])

#%%

df_ec_lmb = pd.read_csv(r'C:\Users\aspit\Git\MHDLab-Projects\Energy Storage Analysis\datasets\pdf\kim_2013\output\couples.csv', index_col=0)

df_ec_lmb = df_ec_lmb.dropna(subset=['C_kwh'])
df_ec_lmb.index.name = 'index_name'

df_ec_lmb = df_ec_lmb[['C_kwh']]

df_ec_lmb['energy_type'] = "EC Couples (LMB)"
df_vis = pd.concat([df_vis, df_ec_lmb])

#%%
cat_label = 'energy_type'

from matplotlib import ticker as mticker
plt.rcParams.update({'font.size': 20})

df_vis['C_kwh_log'] = np.log10(df_vis['C_kwh'])

fig = plt.figure(figsize = (13,8))
# plt.violinplot(dataset=df_all['C_kwh'].values)
# sns.violinplot(data=df_all, x='cat_label', y='C_kwh_log')
sns.stripplot(data=df_vis, x=cat_label, y='C_kwh_log', size=10)

plt.axhline(np.log10(10), linestyle='--', color='gray')

fig.axes[0].yaxis.set_major_formatter(mticker.StrMethodFormatter("$10^{{{x:.0f}}}$"))
fig.axes[0].yaxis.set_ticks([np.log10(x) for p in range(-1,4) for x in np.linspace(10**p, 10**(p+1), 10)], minor=True)
# plt.gca().set_xticks(np.arange(0, len(labels)), labels=labels)

# plt.yscale('log')
plt.xticks(rotation=45)
plt.ylabel('Material Energy Cost ($/kWh)')
plt.tight_layout()
plt.savefig('output/fig_C_kwh_avgprice.png')
# %%

val_counts = df_prices['num_source'].value_counts()
present_num_sources = val_counts.index

val_counts

#%%

dfs_price_refs = []

for n in present_num_sources:
    df_prices_refs = df_prices
    df_sel = df_prices.where(df_prices['num_source'] == n)
    df_sel = df_sel['specific_price_refs'].dropna().rename('specific_price').to_frame()
    df_sel['price_type'] = '{} references'.format(n)
    dfs_price_refs.append(df_sel)
#%%

# df_prices_refs = df_prices['specific_price_refs'].dropna().rename('specific_price').to_frame()
# df_prices_refs['price_type']= 'reference'
df_prices_element = df_prices['specific_price_element'].dropna().rename('specific_price').to_frame()
df_prices_element['price_type']= 'elemental'


df_prices_2 = pd.concat([
    *dfs_price_refs,
    df_prices_element
])

# df_prices_2 = df_prices_2.reset_index()

df_prices_2

#Downselect to those preset
df_prices_2 = df_prices_2.loc[set(df_sp_energy['index_name'])]

df_prices_2

#%%

df_vis = pd.merge(df_prices_2, df_sp_energy, on='index_name')

df_vis['C_kwh'] = df_vis['specific_price']/df_vis['specific_energy']

df_vis
# %%
cat_label = 'energy_type'

from matplotlib import ticker as mticker
plt.rcParams.update({'font.size': 20})

df_vis['C_kwh_log'] = np.log10(df_vis['C_kwh'])

fig = plt.figure(figsize = (13,8))
# plt.violinplot(dataset=df_all['C_kwh'].values)
# sns.violinplot(data=df_all, x='cat_label', y='C_kwh_log')
sns.stripplot(data=df_vis, x=cat_label, y='C_kwh_log', hue='price_type', size=10)

plt.axhline(np.log10(10), linestyle='--', color='gray')

fig.axes[0].yaxis.set_major_formatter(mticker.StrMethodFormatter("$10^{{{x:.0f}}}$"))
fig.axes[0].yaxis.set_ticks([np.log10(x) for p in range(-1,4) for x in np.linspace(10**p, 10**(p+1), 10)], minor=True)
# plt.gca().set_xticks(np.arange(0, len(labels)), labels=labels)

# plt.yscale('log')
plt.xticks(rotation=45)
plt.ylabel('Material Energy Cost ($/kWh)')
plt.tight_layout()

plt.savefig('output/fig_C_kwh.png')

# %%
