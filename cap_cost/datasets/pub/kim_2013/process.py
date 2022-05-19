#%%
import os
import pandas as pd
from es_utils.units import convert_units, prep_df_pint_out, ureg

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

df_price = df_price.astype({
    'specific_price': 'pint[USD/kg]',
    })
df_price = convert_units(df_price)
df_price = prep_df_pint_out(df_price)

df_price.to_csv('output/mat_data.csv')


#%%
from es_utils.pdf import average_range

import numpy as np

df_table3 = pd.read_csv('tables/table_3.csv', index_col=0)
# df_table3.replace(np.nan, '0-0')#.apply(average_range)

df_table3 = df_table3.replace(np.nan,'')

for column in df_table3.columns:
    df_table3[column] = df_table3[column].astype(str).apply(average_range)

df_table3 = df_table3.replace('',np.nan)

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


#Calculate the valence and mole fractions based on section 3.1.1 in the text
#TODO: I'm not sure if I'm doing this right. in particular I don't understand eq. 10, and if that works with the way molar fracitons are calculated in our framework.
valences = {
    'Mg': 2, 
    'Ba': 2, 
    'Ca': 2, 
    'K': 1, 
    'Na': 1, 
    'Li': 1
}

df_couples['n_e'] = [valences[A] for A in df_couples['A'].values]

x_Ad = df_couples['n_e']/(1+df_couples['n_e'])
x_Bd = 1 - x_Ad

# df_couples['materials'] = "[('" + df_couples['A'] + "', 1), ('" + df_couples['B'] + "', 1)]"
df_couples['materials'] = "[('" + df_couples['A'] + "', " + x_Ad.astype(str) +"), ('" + df_couples['B'] + "', " + x_Bd.astype(str) + ")]"
df_couples['materials'] = df_couples['materials'].astype(str)

df_couples = df_couples.drop(['A', 'B'], axis=1)
df_couples = df_couples.rename({'index': 'original_name'}, axis=1)

df_couples['SM_type'] = 'liquid_metal_battery'
df_couples['mat_basis'] = 'molar'

df_couples.index.name = 'SM_name'

df_couples = df_couples.astype({
    'deltaV': 'pint[V]',
    'n_e': 'pint[dimensionless]'
    })
df_couples = convert_units(df_couples)
df_couples = prep_df_pint_out(df_couples)


df_couples.to_csv('output/SM_data.csv')
#%%





