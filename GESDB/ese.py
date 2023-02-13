"""
Data pulled manually from tables at http://www.energystorageexchange.org/projects/ to compare
"""

#%%

import pandas as pd
import os

fns = os.listdir('ese/input')

dfs = []
for fn in fns:
    df = pd.read_csv(os.path.join('ese/input',fn))
    dfs.append(df)


df = pd.concat(dfs)
df = df.reset_index(drop=True)
df = df.drop('Unnamed: 0', axis=1)

df.columns = ['name', 'type', 'power','duration','status','unkown','date']

df['power'] = df['power'].str.replace(',','').astype(int)
df['name'] = df['name'].str.replace('NaN class=\'normalblue\'>', '')
# %%
df['type'].value_counts().to_csv('ese/type_counts.csv')

#%%

# df['energy'] = df['power']*df['dur']

# df['hours'], df['minutes'] = df['duration'].str.split(':', expand=True)

df[['hours', 'minutes']] = df['duration'].str.split(':', expand=True)
df['hours'] = df['hours'].astype(float) + df['minutes'].astype(float)/60

df = df.drop('minutes', axis=1)
# df['minutes']

# pd.to_datetime(df['duration'].str.replace('0:','00:'), format='HH:MM')
# %%

# df
df['energy'] = df['hours']*df['power']

# %%

# df.sort_values('energy')


# df.dropna(subset=['energy']).sort_values('energy')

# df.to_csv('ese.csv')
# %%

df2 = df


# df2 = df2.where(df2['status'] == 'Operational').dropna(how='all')

#%%

energies = df2.groupby('type')['energy'].sum().sort_values(ascending=False)

energies

#%%


energies.iloc[:10].plot.bar()

#%%

import matplotlib.pyplot as plt

energies.iloc[0:15].plot.bar()


plt.yscale('log')
plt.ylabel('total capacity (kWh)')
# %%

top_energy_idx = energies.iloc[:10].index

df2.groupby(['type','status'])['status'].count().loc[top_energy_idx]

# %%

# status_types = set(df2['status'])


status_types = [
 'Announced',
 'Announced/Never Built',
 'Contracted',
 'De-Commissioned',
 'Offline/Under Repair',
 'Under Construction',
 'Operational'
 ]

fig, axes = plt.subplots(len(status_types), 1, figsize=(5,15), sharex=True , sharey=True)

for i, status in enumerate(status_types):
    df_subset = df2.where(df2['status'] == status).dropna(how='all')
    energies = df_subset.groupby('type')['energy'].sum().sort_values(ascending=False)

    energies.iloc[:10].plot.bar(ax =axes[i])
    axes[i].set_title(status)
    axes[i].set_yscale('log')

plt.tight_layout()
plt.savefig('ese/type_counts.png')
