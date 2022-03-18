#%%
#%%
import pandas as pd
import matplotlib.pyplot as plt


import seaborn as sns

df = pd.read_csv('output/processed.csv', index_col=0)

sns.scatterplot(data=df, x='min_quantity_kg', y='specific_price')
plt.xscale('log')
plt.yscale('log')

plt.savefig('figures/price_vs_minquantity.png')

# %%
df.index.value_counts()
#%%
