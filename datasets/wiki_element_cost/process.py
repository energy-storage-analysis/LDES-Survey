#%%
from re import I
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt

import sys

from es_utils import average_range

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

from pyvalem.formula import Formula
df['molar_mass'] = [Formula(s).rmm for s in df['Symbol']] 

# %%
df[['Symbol', 'Name', 'cost','molar_mass']].to_csv('output/process.csv')
# %%
