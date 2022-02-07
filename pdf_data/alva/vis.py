#%%
import pandas as pd
import matplotlib.pyplot as plt
import sys
sys.path.append('..')
import pdf_utils



df = pd.read_csv('output/table_8.csv')

#df = pdf_utils.concat_row_to_columns(df, 3)

df = df.rename(
    {'Type  ': 'type',
       'Class  ': 'class', 
       'Thermal storage material  ': 'material',
       'Phase change temperature (degC) ': 'phase_change_T',
       'Latent heat (kJ$kg\n-1) ': 'sp_latent_heat',
       '-3)\nDensity (kg$m  ': 'density',
       'Thermal conductivity (W$m\n-1 K\n-1)': 'therm_conductivity',
       'Latent heat storage capacity (MJ$m\n-3) ': 'vol_latent_heat',
       'Technical grade cost ($$kg\n-1) ': 'cost',
       'Remarks  ':'remarks'},
axis=1)

df = df.drop('type',axis=1)
df = df.drop('Unnamed: 0',axis=1)
df = df.drop('remarks',axis=1)

df['phase_change_T'] = df['phase_change_T'].replace('40-45', '42.5')
df['phase_change_T'] = df['phase_change_T'].astype(float)

df['sp_latent_heat'] = df['sp_latent_heat'].astype(float)

df['class'] = df['class'].fillna(method='ffill') 
df['class'] = df['class'].replace('eutectics', 'Organic', regex=True)
df['class'] = df['class'].replace('Organic', 'Organic Eutectic', regex=True)
df['class'] = df['class'].replace('Inorganic ', '', regex=True)
df['cost'] = df['cost'].dropna().replace('\(RG\)','', regex=True).astype(float)

df.info()
#%%
df['class'].value_counts().plot(kind='bar')
#%%

df_phys = df[['class','cost','sp_latent_heat']]
df_phys
#%%
import seaborn as sns

sns.boxplot(x='class',y='cost',data=df_phys)
plt.xticks(rotation=90)
plt.yscale('log')
#%%

df_plot = df_phys#.where(df_phys['class'] == 'Glycols')

plt.figure(figsize = (15,6))
sns.swarmplot(x='class',y='sp_latent_heat',data=df_plot)
plt.xticks(rotation=90)

plt.yscale('log')
#%%

plt.figure(figsize = (15,6))
sns.violinplot(x='class',y='sp_latent_heat',data=df_phys)
plt.xticks(rotation=90)
plt.yscale('log')
plt.ylim(1e1,)
# plt.ylim(0,)
 # %%
# %%
import numpy as np
bins = np.logspace(np.log10(8e1), np.log10(1e3), 30)
df['sp_latent_heat'].hist(bins=bins)
plt.xscale('log')
plt.xlabel('Latent Heat (kJ/kg')
#%%

bins = np.logspace(np.log10(1e0), np.log10(2e3), 30)
df['cost'].hist(bins=bins)
plt.xscale('log')
plt.xlabel('Cost ($/kg)')

#%%
from pandas.plotting import scatter_matrix
scatter_matrix(df, figsize=(10,10))
#%%

cols = ['class','sp_latent_heat','cost']
df_sel = df.dropna(subset=cols, how='any')[cols]
df_sel = df_sel.sort_values('cost')
g = sns.scatterplot(data=df_sel, x='cost', y='sp_latent_heat', hue='class')
plt.xscale('log')

plt.gca().get_legend().set_bbox_to_anchor([0,0,1.5,1])

#plt.locator_params(axis='x', nbins=5)
#g.set_xticklabels(rotation=45)
#s = df_sel.set_index(['class','cost'])['sp_latent_heat']
#s.groupby('class').plot(x='cost')
#plt.legend()
