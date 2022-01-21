#%%
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('output/table_8.csv')

df = df.rename(
    {'Table 8 Phase change materials [17]. Type  ': 'type',
       '  Class  ': 'class', 
       '  Thermal storage material  ': 'material',
       '  Phase change temperature (degC) ': 'phase_change_T',
       '  Latent heat (kJ$kg\n-1) ': 'latent_heat',
       '  -3)\nDensity (kg$m  ': 'density',
       '  Thermal conductivity (W$m\n-1 K\n-1)': 'therm_conductivity',
       '  Latent heat storage capacity (MJ$m\n-3) ': 'capacity',
       '  Technical grade cost ($$kg\n-1) ': 'cost',
       '  Remarks  ':'remarks'},
axis=1)

df = df.drop('type',axis=1)
df = df.drop('Unnamed: 0',axis=1)
df

df['class'] = df['class'].fillna(method='ffill') 
df['class'] = df['class'].replace('eutectics', 'Organic', regex=True)
df['class'] = df['class'].replace('Organic', 'Organic Eutectic', regex=True)
df['class'] = df['class'].replace('Inorganic ', '', regex=True)
df['cost'] = df['cost'].dropna().replace('\(RG\)','', regex=True).astype(float)
# %%
df['class'].value_counts().plot(kind='bar')
#%%

# %%
# %%
df_phys = df[['class','cost','latent_heat']]
df_phys
#%%
import seaborn as sns

sns.boxplot(x='class',y='cost',data=df_phys)
plt.xticks(rotation=90)
plt.yscale('log')
#%%

df_plot = df_phys#.where(df_phys['class'] == 'Glycols')

plt.figure(figsize = (15,6))
sns.swarmplot(x='class',y='latent_heat',data=df_plot)
plt.xticks(rotation=90)

plt.yscale('log')
#%%

plt.figure(figsize = (15,6))
sns.violinplot(x='class',y='latent_heat',data=df_phys)
plt.xticks(rotation=90)
plt.yscale('log')
plt.ylim(1e1,)
# plt.ylim(0,)
 # %%
# %%
import numpy as np
bins = np.logspace(np.log10(8e1), np.log10(1e3), 30)
df['latent_heat'].hist(bins=bins)
plt.xscale('log')
plt.xlabel('Latent Heat (kJ/kg')
#%%

bins = np.logspace(np.log10(1e0), np.log10(2e3), 30)
df['cost'].hist(bins=bins)
plt.xscale('log')
plt.xlabel('Cost ($/kg)')
# %%
