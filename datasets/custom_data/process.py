import pandas as pd
import os

if not os.path.exists('output'):
    os.mkdir('output')

df_custom_prices = pd.read_csv('custom_prices.csv',index_col=0)
df_custom_prices.to_csv('output/mat_prices.csv')

df_custom_physprop = pd.read_csv('custom_physprop.csv',index_col=0)

phys_prop_names = set(df_custom_physprop['physprop_name'].values)

df_physprops = pd.DataFrame(index=df_custom_physprop.index, columns=phys_prop_names)

for idx,row in df_custom_physprop.iterrows():
    physprop_name = row['physprop_name']
    df_physprops[physprop_name].loc[idx] = row['physprop_value']

df_physprops[['original_name','source']] = df_custom_physprop[['original_name','source']] 

df_physprops.to_csv('output/physprop.csv')

