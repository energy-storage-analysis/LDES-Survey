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
pdf_path = os.path.join(pdf_folder, r"Liu et al_2016_Review on concentrating solar power plants and new developments in high.pdf")

template_path = 'tabula_template.json'
with open(template_path, 'r') as f:
    templates= json.load(f)

template_path = 'extract_settings.json'
with open(template_path, 'r') as f:
    extract_settings= json.load(f)

for i in range(len(extract_settings)):
    extract_settings[i]['template'] = templates[i]

    if 'camelot_kwargs' not in extract_settings[i]: extract_settings[i]['camelot_kwargs'] = {}
    extract_settings[i]['camelot_kwargs'].update({'flavor': 'stream'})
#%%

dfs = es_utils.pdf.extract_dfs(pdf_path, extract_settings)
#%%
tables = {}

tables['table_2'] = dfs[0]
#%%
df_table4 = pd.concat([dfs[1],dfs[2]]).reset_index(drop=True)

df_table4 = df_table4.replace('\[71\]','', regex=True)

df_table4 = df_table4.drop([13,15,17])

df_table4.iloc[0]['Cost/kg ($US/kg)'] = df_table4.iloc[0]['Cost/kg ($US/kg)'] + ' [Sand]'

df_split = df_table4['Cost/kg ($US/kg)'].str.split('[', expand=True)

df_table4['Cost/kg ($US/kg)'] = df_split[0]
df_table4['name'] = df_split[1].str.strip('] ')



df_table4

#%%

tables['table_4'] = df_table4

#%%



# %%

output_folder = 'tables'
if not os.path.exists(output_folder): os.mkdir(output_folder)

for fn in os.listdir(output_folder):
    os.remove(os.path.join(output_folder, fn))

for table in tables:
    tables[table].to_csv('{}/{}.csv'.format(output_folder, table))
# %%
