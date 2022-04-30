#%%

from jmespath import search
import pandas as pd


mat_data_path = r'C:\Users\aspit\Git\MHDLab-Projects\Energy-Storage-Analysis\cap_cost\data_consolidated\mat_data.csv'
mat_data = pd.read_csv(mat_data_path, index_col=0)
mat_data_used = mat_data[mat_data['num_SMs'] > 0]

search_list_path = r'C:\Users\aspit\Git\MHDLab-Projects\Energy-Storage-Analysis\cap_cost\datasets\alibaba\scrapy_alibaba\resources\mat_data_searches.csv'
search_list = pd.read_csv(search_list_path, index_col=0)


# %%

missing_searches = [s for s in mat_data.index if s not in search_list.index]
missing_searches

# %%
bulkpath = r'C:\Users\aspit\Git\MHDLab-Projects\Energy-Storage-Analysis\cap_cost\datasets\alibaba\bulk\output\mat_data.csv'
mat_bulk = pd.read_csv(bulkpath, index_col=0)
mat_bulk

used_bulk = mat_bulk.loc[[i for i in mat_bulk.index if i in mat_data_used.index]]
used_bulk = list(set(used_bulk.index))
used_bulk


#%%


missing_searches = [s for s in used_bulk if s not in search_list.index]
missing_searches
s = pd.Series(list(set(missing_searches))).to_csv('temp.csv')