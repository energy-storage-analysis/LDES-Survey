"""Simple script to output a table dealing with a specific technology"""

#%%
import pandas as pd
import os

output_dir = 'output'
if not os.path.exists(output_dir): os.makedirs(output_dir)


df_SMs = pd.read_csv('../data_consolidated/SM_data.csv', index_col=[0,1])
df = df_SMs.reset_index('SM_type')


df = df.where(df['SM_type'].isin([
    'flow_battery',
    'hybrid_flow'
])).dropna(subset=['SM_type'])


df = df.dropna(axis=1, how='all')

df.to_csv(os.path.join(output_dir,'SM_type_downsel.csv'))