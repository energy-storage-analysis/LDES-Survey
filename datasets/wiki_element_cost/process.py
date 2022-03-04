#%%
from re import I
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt

import sys
sys.path.append('../pdf')
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


#%%

df = df[df['Symbol'].isin(['2H (D)', '99mTc', '147Pm']) == False]
df

# %%


# %%
df[['Symbol', 'Name', 'cost']].to_csv('output/process.csv')