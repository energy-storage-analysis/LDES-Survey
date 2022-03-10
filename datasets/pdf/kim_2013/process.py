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

df_table4.reset_index().rename({'metal':'molecular_formula'},axis=1).to_csv('output/prices.csv', index=False)

df_table4
#%%

import sys
sys.path.append('..')
from pdf_utils import average_range

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
        s_deltaV.loc['{}-{}'.format(metal_A,metal_B)] = deltaV

df_couples = s_deltaV.to_frame()
df_couples['index'] = df_couples.index
df_couples[['metal_A','metal_B']] = df_couples['index'].str.split('-',expand=True)
df_couples = df_couples.drop('index', axis=1)
df_couples
# %%
df_couples['mm_A'] = df_table4.loc[df_couples['metal_A']]['molar_mass'].values
df_couples['mm_B'] = df_table4.loc[df_couples['metal_B']]['molar_mass'].values


df_couples['SP_A'] = df_table4.loc[df_couples['metal_A']]['specific_price'].values
df_couples['SP_B'] = df_table4.loc[df_couples['metal_B']]['specific_price'].values

df_couples

#%%

F = 96485 # C/mol

#TODO: chech this equation
df_couples['specific_price'] = (df_couples['SP_A']*df_couples['mm_A'] + df_couples['SP_B']*df_couples['mm_B'])/(df_couples['mm_A']+df_couples['mm_B'])



df_couples['specific_energy'] = (1/3600)*F*df_couples['deltaV']/(df_couples['mm_A'] + df_couples['mm_B'])
df_couples['C_kwh'] = df_couples['specific_price']/df_couples['specific_energy']
df_couples

#%%


df_couples.to_csv('output/couples.csv')

