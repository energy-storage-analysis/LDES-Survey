#%%
import pandas as pd
import matplotlib.pyplot as plt
import sys
sys.path.append('..')
import pdf_utils



df = pd.read_csv('output/table_2.csv', index_col=0)

df.info()
#%%
df['type'].value_counts().plot(kind='bar')
#%%

df_phys = df[['type','C_kwh','year']]
df_phys
#%%
import seaborn as sns

sns.boxplot(x='type',y='C_kwh',data=df_phys)
plt.xticks(rotation=90)
plt.yscale('log')
#%%

df_plot = df_phys#.where(df_phys['class'] == 'Glycols')

plt.figure(figsize = (15,6))
sns.swarmplot(x='type',y='C_kwh',data=df_plot)
plt.xticks(rotation=90)

plt.yscale('log')
#%%

plt.figure(figsize = (15,6))
sns.violinplot(x='type',y='C_kwh',data=df_phys)
plt.xticks(rotation=90)
# plt.yscale('log')
# plt.ylim(1e1,)
# plt.ylim(0,)
 # %%
# %%
import numpy as np
bins = np.logspace(np.log10(8e1), np.log10(1e3), 30)
df['C_kwh'].hist(bins=bins)
plt.xscale('log')
plt.xlabel('C_kwh')
#%%
from pandas.plotting import scatter_matrix
scatter_matrix(df, figsize=(10,10))
#%%

cols = ['type','year','C_kwh']
df_sel = df.dropna(subset=cols, how='any')[cols]
df_sel = df_sel.sort_values('C_kwh')
g = sns.scatterplot(data=df_sel, y='C_kwh', x='year', hue='type')
plt.yscale('log')
plt.xlim(1950,)

plt.gca().get_legend().set_bbox_to_anchor([0,0,1.5,1])

#plt.locator_params(axis='x', nbins=5)
#g.set_xticklabels(rotation=45)
#s = df_sel.set_index(['class','C_kwh'])['sp_latent_heat']
#s.groupby('class').plot(x='C_kwh')
#plt.legend()

#%%
df_table3 = pd.read_csv('output/table_3.csv', index_col=0)

df_table3
#%%

df_table3['C_kwh'].hist()
#%%

plt.figure(figsize = (15,6))
sns.violinplot(y='C_kwh',data=df_phys)
plt.xticks(rotation=90)
# %%
