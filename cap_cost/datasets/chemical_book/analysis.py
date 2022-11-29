
#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('output/extracted.csv', index_col=0)

df
# %%

bins = np.logspace(-3,1, 15)


df['min_quantity_kg'].hist(bins=bins)
plt.xscale('log')
# %%

df.plot.scatter(x='min_quantity_kg',y='specific_price')
plt.xscale('log')
plt.yscale('log')


#%%

df.groupby('manufacturer')['min_quantity_kg'].mean().sort_values().plot.bar()