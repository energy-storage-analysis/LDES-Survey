#%%
from re import I
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt

import sys
sys.path.append('..')
from pdf_utils import average_range

df = pd.read_csv('table_element_cost.csv', index_col=0)

df = df.loc[0:83]

df = df.rename({
    'USD/kg': 'cost'
}, axis=1)

df.info()



df['cost'] = df['cost'].replace(' ','', regex=True)
df['cost'] = df['cost'].apply(average_range).replace('Not traded.', np.nan, regex=True).dropna()


df['cost'] = df['cost'].replace('×1012', 'e12', regex=True)
df['cost'] = df['cost'].astype(float)

# df = df.where(df['cost'] < 1e12).dropna(subset=['cost'])

# %%

bins = np.logspace(np.log10(0.1), np.log10(1e13), 50)

df['cost'].hist(bins=bins)
plt.xscale('log')
# %%


df_high = df.where(df['cost'] >1e3).dropna()
df_high[['Name','cost']].sort_values('cost')
#%%
df_low = df.where(df['cost'] <10).dropna()
df_low[['Name','cost']].sort_values('cost')

# %%
df[['Symbol', 'Name', 'cost']].to_csv('table_out.csv')