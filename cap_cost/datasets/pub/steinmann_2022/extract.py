#%%
import os
import pandas as pd
import json
import es_utils

#PDF location info
pdf_folder = r'C:\Users\aspit\OneDrive\Literature\Zotero\Energy Storage'
pdf_fn =  r"Steinmann_2022_Thermal Energy Storage for Medium and High Temperatures.pdf"
pdf_path = os.path.join(pdf_folder,pdf_fn)

#This is the default 'flavor' for the table extraction (lattice = table has lines, stream = opposite)
DEFAULT_FLAVOR = 'stream'

template_path = 'tabula_template.json'
with open(template_path, 'r') as f:
    templates= json.load(f)

template_path = 'extract_settings.json'
with open(template_path, 'r') as f:
    extract_settings= json.load(f)

for i in range(len(extract_settings)):
    extract_settings[i]['template'] = templates[i]

    if 'camelot_kwargs' not in extract_settings[i]: extract_settings[i]['camelot_kwargs'] = {}
    extract_settings[i]['camelot_kwargs'].update({'flavor': DEFAULT_FLAVOR ,'row_tol': 10})
#%%

dfs = es_utils.pdf.extract_dfs(pdf_path, extract_settings)
#%%

#Setup table dictionary and do any processing here. 

tables = {}

# tables = {'table_{}'.format(i+1): dfs[i] for i in range(len(dfs))}

tables['table_21'] = dfs[0]
tables['table_22'] = dfs[1]
tables['table_23'] = dfs[2]
tables['table_31'] = dfs[3]
tables['table_32'] = dfs[4]
tables['table_37'] = dfs[5]
tables['table_311'] = dfs[6]
tables['table_61'] = dfs[7]
tables['table_62'] = dfs[8]
tables['table_63'] = dfs[9]
tables['table_72'] = dfs[10]
tables['table_73'] = dfs[11]

# %%

output_folder = 'tables'
if not os.path.exists(output_folder): os.mkdir(output_folder)

for fn in os.listdir(output_folder):
    os.remove(os.path.join(output_folder, fn))

for table in tables:
    for column in tables[table].columns:
        tables[table][column] = tables[table][column].str.replace('–','-')
        tables[table][column] = tables[table][column].str.replace('−','-')

    tables[table].to_csv('{}/{}.csv'.format(output_folder, table), index=False)
# %%
