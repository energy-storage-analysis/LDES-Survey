"""
Various stats calculations for synopsis

Number of citations#
Number of energy density calculations:
Number of material prices obtained:
Number of cost of storage determined:
"""
#%%
from es_utils.units import read_pint_df, ureg

import os
from os.path import join as pjoin
output_dir = 'tables'
if not os.path.exists(output_dir): os.makedirs(output_dir)

from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

df_SMs = read_pint_df(pjoin(REPO_DIR,'cap_cost/data_consolidated/SM_data.csv'), index_col=[0,1])#.reset_index('SM_type')

df_mat_data = read_pint_df(pjoin(REPO_DIR, 'cap_cost/data_consolidated/mat_data.csv'), index_col=0, drop_units=True)
df_mat_data_all = read_pint_df(pjoin(REPO_DIR, 'cap_cost/data_consolidated/mat_data_all.csv'), index_col=0, drop_units=True)

# Note that Fossil CH4 datapoint is included in data, can be removed here. 
# df_SMs = df_SMs.drop(('Fossil CH4', 'synfuel'))
# df_mat_data = df_mat_data.drop('Fossil CH4')

stats = {}

#%%

#%%
import pandas as pd

df_mat_unused = pd.read_csv('tables/mat_data_unused.csv', index_col=0)
df_mat_used = pd.read_csv('tables/mat_data_used.csv', index_col=0)






#%%
# df_SMs['SM_sources'].value_counts()




# SM_source_info = df_SMs.groupby('SM_sources')['SM_type'].apply(get_source_SM_counts).dropna()
# SM_source_info.name = 'SM types'

# price_source_info = df_mat_data.groupby('sources').apply(len)
# price_source_info.name = 'num prices'


source_lists = df_SMs['SM_sources'].dropna().apply(lambda x: x.split(',')).values
SM_source_list = set([item.strip() for sublist in source_lists for item in sublist])

source_lists = df_mat_data['sources'].dropna().apply(lambda x: x.split(',')).values
mat_source_list = set([item.strip() for sublist in source_lists for item in sublist])

#%%

for r in ['Synfuel feedstock', 'Standard Gibbs', 'Cryo tank', 'Cavern']:
    SM_source_list.remove(r)

SM_source_list = list(SM_source_list)
SM_source_list.append('Engineering Toolbox')

SM_source_list = pd.DataFrame(index=SM_source_list)
SM_source_list['physprop'] = 'Yes'

mat_source_list = pd.DataFrame(index=mat_source_list)
mat_source_list['mat_prices'] = 'Yes'


df_out = pd.concat([SM_source_list, mat_source_list], axis=1).fillna('No')
df_out.index.name = 'Source'

df_out.to_csv('tables/source_list.csv')


#%%

stats['num_mat_raw_all'] = len(df_mat_data_all)
stats['num_mat_raw_used'] = len(df_mat_data_all.loc[df_mat_used.index])
stats['num_mat_avg_all'] = len(df_mat_used) + len(df_mat_unused)
stats['num_mat_avg_used'] = len(df_mat_used) 

# stats['num_SM'] = len(df_SMs)
stats['num_energy_density'] = len(df_SMs['specific_energy'].dropna())
stats['num_cost_of_storge'] = len(df_SMs['specific_price'].dropna())
stats['num_Ckwh'] = len(df_SMs['C_kwh'].dropna())
stats['num_sources'] = len(df_out)


long_name_dict = {
'num_mat_raw_all' : "Number of all obtained individual material prices",
'num_mat_raw_used' : "Number of all individual material prices used",
'num_mat_avg_all' : "Number of all material price averages",
'num_mat_avg_used' : "Number of all material price averages used",
'num_energy_density' : "Number of storage medium energy density calculations",
'num_cost_of_storge' : "Number of storage medium specific price",
'num_Ckwh' : "Number of storage medium energy capital cost (C_kWh,SM)",
'num_sources' : "Number of sources used to form the dataset",
}



s_stats = pd.Series(stats)
s_stats.name = 'Count'

s_long_name = pd.Series(long_name_dict)
s_long_name.name = 'Description'

df_stats = pd.concat([s_stats, s_long_name], axis=1)

df_stats = df_stats.set_index('Description', drop=True)

df_stats.to_csv('tables/dataset_counts.csv')