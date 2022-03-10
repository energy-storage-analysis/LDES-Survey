#%%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('output/couples.csv', index_col=0)
df=  df.dropna(subset=['deltaV'])

df.sort_values('C_kwh')

#%%

bins = np.logspace(np.log10(1), np.log10(1e6), 50)
df['C_kwh'].hist(bins=bins)

plt.xscale('log')
# %%
