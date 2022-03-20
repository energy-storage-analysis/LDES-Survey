from ntpath import join
import pandas as pd
import os

from sympy import O

if not os.path.exists('output'):
    os.mkdir('output')

df_custom_prices = pd.read_csv('custom_prices.csv',index_col=0)
# df_custom_prices.to_csv('output/mat_prices.csv')

df_custom_physprop = pd.read_csv('custom_physprop.csv',index_col=0)

phys_prop_names = set(df_custom_physprop['physprop_name'].values)

df_physprops = pd.DataFrame(index=set(df_custom_physprop.index), columns=phys_prop_names)
df_physprops.index.name = 'index'
# df_physprops =df_physprops.drop_duplicates()

for idx,row in df_custom_physprop.iterrows():
    physprop_name = row['physprop_name']
    df_physprops[physprop_name].loc[idx] = row['physprop_value']


from es_utils import join_col_vals
df_physprops['source'] = df_custom_physprop.groupby('index').apply(join_col_vals, column='source')


#TODO: implement physprop
df_physprops['original_name'] = df_physprops.index


df_mat_data = pd.concat([
    df_custom_prices,
    df_physprops,
], axis=1)

df_mat_data.to_csv('output/mat_data.csv')


