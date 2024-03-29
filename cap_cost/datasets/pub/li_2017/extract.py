#%%
import os
from matplotlib.pyplot import table
import pandas as pd
import camelot
import json
import sys


import es_utils


from dotenv import load_dotenv
load_dotenv()

pdf_folder = os.getenv('PDF_FOLDER_PATH')
pdf_path = os.path.join(pdf_folder, r"Li et al_2017_Air-Breathing Aqueous Sulfur Flow Battery for Ultralow-Cost Long-Duration2.pdf")

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

dfs = es_utils.pdf.extract_dfs(pdf_path, extract_settings)

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

#TODO: improve
df_table2['type'] = df_table2['type'].str.replace('\n','')
df_table2['type'] = df_table2['type'].str.replace('\r','')
df_table2['ancat'] = df_table2['ancat'].str.replace('\n','')
df_table2['ancat'] = df_table2['ancat'].str.replace('\r','')
df_table2['label'] = df_table2['label'].str.replace('\n','')
df_table2['label'] = df_table2['label'].str.replace('\r','')
df_table2['ref'] = df_table2['ref'].str.replace('\n','')
df_table2['ref'] = df_table2['ref'].str.replace('\r','')

df_table2['ancat'] = df_table2['ancat'].str.replace('F-','Fe') #TODO: looks like regex to replace 'e' in table extraction accidentally gets Fe with charge \d+-, but don't want to change without testing other tables. 


tables['table_2'] = df_table2
#%%
import numpy as np

df_table3 = pd.concat([dfs[2], dfs[3]], axis=0)


df_table3 = df_table3.drop(' ', axis=1)

df_table3 = df_table3.rename(
    {
    ' Chemical': 'original_name', 
    ' Price \n(US$/kg)': 'specific_price', 
    ' Source': 'ref'
    },
axis=1)


df_table3['original_name'] = df_table3['original_name'].replace('',np.nan)
df_table3 = df_table3.dropna(subset=['original_name'])

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
