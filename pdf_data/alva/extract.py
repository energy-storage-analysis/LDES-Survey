#%%
import os
from matplotlib.pyplot import table
import pandas as pd
import camelot
import json
import sys

sys.path.append('..')
import pdf_utils

# pdf_folder = r'/media/lee/Shared Storage/table_extract_text'
pdf_folder = r'C:\Users\aspit\OneDrive\Literature\Zotero\Energy Storage'
pdf_path = os.path.join(pdf_folder, r"Alva et al_2018_An overview of thermal energy storage systems.pdf")

template_path = 'tabula_template.json'
with open(template_path, 'r') as f:
    templates= json.load(f)

template_path = 'extract_settings.json'
with open(template_path, 'r') as f:
    extract_settings= json.load(f)

for i in range(len(extract_settings)):
    extract_settings[i]['template'] = templates[i]

    if 'camelot_kwargs' not in extract_settings[i]: extract_settings[i]['camelot_kwargs'] = {}
    extract_settings[i]['camelot_kwargs'].update({'flavor': 'stream', 'row_tol':5})

#%%

dfs = pdf_utils.extract_dfs(pdf_path, extract_settings)

dfs[0]

#%%
table_8_items = [7,8,9,10]
dfs_table_8 = [dfs[i] for i in table_8_items]
dfs_other = [dfs[i] for i in range(len(extract_settings)) if i not in table_8_items]

dfs_table_8[1].columns = dfs_table_8[0].columns
dfs_table_8[2].columns = dfs_table_8[0].columns
dfs_table_8[3].columns = dfs_table_8[0].columns

df_table_8 = pd.concat(dfs_table_8)

dfs_other.insert(7, df_table_8)
# %%

output_folder = 'output'

for fn in os.listdir(output_folder):
    os.remove(os.path.join(output_folder, fn))

for i, df in enumerate(dfs_other):
    output_path = os.path.join(output_folder, 'table_{}.csv'.format(i+1))
    df.to_csv(output_path)
# %%
