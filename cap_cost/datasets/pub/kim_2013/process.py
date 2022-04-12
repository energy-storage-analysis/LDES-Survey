#%%
import os
from re import I
import pandas as pd
from sympy import O

if not os.path.exists('output'): os.mkdir('output')


df_table4 = pd.read_csv('tables/table_4.csv', index_col=0)

#%%
from pyvalem.formula import Formula


df_table4['molar_mass'] = [Formula(f).rmm for f in df_table4.index]
df_table4['specific_price'] = 1000*(df_table4['molar_price']/df_table4['molar_mass'])

df_table4 = df_table4.reset_index().rename({'metal':'molecular_formula'},axis=1)

index_use = 'molecular_formula'
df_table4['index_use'] = index_use
df_table4['index'] = df_table4[index_use]
df_table4 = df_table4.set_index('index')

df_table4['original_name'] = df_table4['molecular_formula']

from es_utils import extract_df_mat
df_price = extract_df_mat(df_table4)
df_price.to_csv('output/mat_data.csv')


#%%

import sys

from es_utils.pdf import average_range

import numpy as np

df_table3 = pd.read_csv('tables/table_3.csv', index_col=0)
# df_table3.replace(np.nan, '0-0')#.apply(average_range)

df_table3 = df_table3.replace(np.nan,'')

for column in df_table3.columns:
    df_table3[column] = df_table3[column].astype(str).apply(average_range)

df_table3 = df_table3.replace('',np.nan)

df_table3


#%%

s_deltaV = pd.Series(dtype=str, name='deltaV')

for metal_B, row in df_table3.iterrows():
    # row = row.dropna()
    for metal_A, deltaV in row.iteritems():
        s_deltaV.loc['{}/{}'.format(metal_A,metal_B)] = deltaV

df_couples = s_deltaV.to_frame()
df_couples['index'] = df_couples.index

#This is in place of a SM lookup
df_couples[['A','B']] = df_couples['index'].str.split('/',expand=True)

df_couples['materials'] = "[('" + df_couples['A'] + "', 0.5), ('" + df_couples['B'] + "', 0.5)]"
df_couples['materials'] = df_couples['materials'].astype(str)

df_couples = df_couples.drop(['A', 'B'], axis=1)
df_couples = df_couples.rename({'index': 'original_name'}, axis=1)

df_couples['SM_type'] = 'liquid_metal_battery'

df_couples.index.name = 'SM_name'

df_couples.to_csv('output/SM_data.csv')
#%%





