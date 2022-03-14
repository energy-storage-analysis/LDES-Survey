from os.path import join as pjoin
import os
from re import I
import pandas as pd

if not os.path.exists('output'): os.mkdir('output')

#Table A1
df_a1 = pd.read_csv(pjoin('tables','table_a1.csv'), skiprows=[1])

df_a1 = df_a1.rename({
    'Material': 'original_name',
    'Relative cost': 'relative_cost',
    'Yield strength': 'yield_strength'
},axis=1)

df_a1['specific_price'] = df_a1['relative_cost']*1 #TODO:assuming relative cost to 1$/kg

df_a1['specific_strength'] = df_a1['yield_strength']/df_a1['density']





#Table A2
df_a2 = pd.read_csv(pjoin('tables','table_a2.csv'), skiprows=[1])

df_a2 = df_a2.rename({
    'Material': 'original_name',
    'relative cost': 'relative_cost',
},axis=1)

df_a2['specific_price'] = df_a2['relative_cost']*1 #TODO: assuming relative cost to 1$/kg

#TODO: What is T and C? 
df_a2['sigma_theta_avg'] = (df_a2['sigma_theta_T'].astype(float) + df_a2['sigma_theta_C'].astype(float))/2

#TODO: from Kamf thesis it seems like the hoop stress is limiting on a simple approximation level. 
df_a2['specific_strength'] = df_a2['sigma_theta_avg']/df_a2['density']


col_select = ['original_name', 'specific_strength','specific_price']

df = pd.concat([
    df_a1[col_select],
    df_a2[col_select],
])

# df = df.set_index('original_name', drop=True)

df = df.rename({'specific_strength': 'specific_energy'}, axis=1) #Assuming Q=1
df['specific_energy'] = df['specific_energy']/3600  

#%%
mat_lookup = pd.read_csv('chem_lookup.csv', index_col=0)

from es_utils.chem import process_chem_lookup
mat_lookup = process_chem_lookup(mat_lookup)

df = pd.merge(df, mat_lookup, on='original_name').set_index('index')

# df = pd.merge(df, mat_lookup, on='original_name')

df = df.groupby('index')[['specific_energy', 'specific_price']].mean() #TODO: can't think of another way to handle multiple entries for given class of material (i.e. steel)


df['energy_type'] = 'virial_limited'

df.to_csv('output/processed.csv')