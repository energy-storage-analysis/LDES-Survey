"""
This is a currently old/unused script to form a keyword search list from the materials database. I decided to be more controlled in forming the list manually. 
"""

#%%
import os
import numpy as np
import pandas as pd

mat_data_path = r'C:\Users\aspit\Git\MHDLab-Projects\Energy-Storage-Analysis\mat_cost\data\mat_data.csv'

df_mat_data = pd.read_csv(mat_data_path, index_col=0)

df_mat_data
# %%
original_names = df_mat_data['original_names'].str.split(',').explode()
original_names = original_names.dropna()
original_names.name = 'original_name'

df_keywords = original_names.to_frame()


#%%

df_keywords['molecular_formula'] = df_mat_data['molecular_formula'][df_keywords.index]

# %%

search_texts = []
for index, row in df_keywords.iterrows():
    original_name = row['original_name'].strip()
    if len(original_name) < 3:
        search_texts.append(np.nan)
    elif index == original_name:
        search_texts.append(index)
    else:
        search_texts.append(index +' ' + original_name)

df_keywords['search_text'] = search_texts

df_keywords = df_keywords.dropna(subset=['search_text'])
# %%
df_keywords.to_csv('keywords_allmats.csv')
# %%
