#%%
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt


bins = np.logspace(np.log10(0.1), np.log10(1e13), 50)

df = pd.read_csv('output/process.csv')


df['cost'].hist(bins=bins)
plt.xscale('log')
# %%


df_high = df.where(df['cost'] >1e3).dropna()
df_high[['Name','cost']].sort_values('cost')
#%%
df_low = df.where(df['cost'] <10).dropna()
df_low[['Name','cost']].sort_values('cost')
# %%