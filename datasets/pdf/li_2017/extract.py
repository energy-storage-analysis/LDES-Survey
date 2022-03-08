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
pdf_path = os.path.join(pdf_folder, r"Li et al_2017_Air-Breathing Aqueous Sulfur Flow Battery for Ultralow-Cost Long-Duration SI.pdf")

template_path = 'tabula_template.json'
with open(template_path, 'r') as f:
    templates= json.load(f)

template_path = 'extract_settings.json'
with open(template_path, 'r') as f:
    extract_settings= json.load(f)

for i in range(len(extract_settings)):
    extract_settings[i]['template'] = templates[i]

    if 'camelot_kwargs' not in extract_settings[i]: extract_settings[i]['camelot_kwargs'] = {}
    extract_settings[i]['camelot_kwargs'].update({'flavor': 'lattice'})
#%%

dfs = pdf_utils.extract_dfs(pdf_path, extract_settings)

#%%
dfs[2]

#%%
tables = {}

dfs[1].columns = dfs[0].columns
df_table2 = pd.concat([dfs[0], dfs[1]], axis=0)
# df_table2 = df_table2.set_index(' Year')
df_table2 = df_table2.reset_index(drop=True)


df_table2 = df_table2.rename(
    {' Year': 'year', 
    ' Label': 'label', 
    ' CCS \n(US$/kWh)': 'C_kwh',
    ' Anode/Cathode': 'ancat', 
    ' Battery Type': 'type', 
    ' Ref.': 'ref'
    },
axis=1)

df_table2 = df_table2.drop(' ',axis=1)


tables['table_2'] = df_table2
#%%
import numpy as np

df_table3 = pd.concat([dfs[2], dfs[3]], axis=0)


df_table3 = df_table3.drop(' ', axis=1)

df_table3 = df_table3.rename(
    {
    ' Chemical': 'full_name', 
    ' Price \n(US$/kg)': 'specific_price', 
    ' Source': 'ref'
    },
axis=1)


df_table3['full_name'] = df_table3['full_name'].replace('',np.nan)
df_table3 = df_table3.dropna(subset=['full_name'])

df_table3 = df_table3.reset_index(drop=True)



tables['table_3'] = df_table3

# %%

output_folder = 'tables'
if not os.path.exists(output_folder): os.mkdir(output_folder)

for fn in os.listdir(output_folder):
    os.remove(os.path.join(output_folder, fn))

for table in tables:
    tables[table].to_csv('{}/{}.csv'.format(output_folder, table), index=False)
# %%
