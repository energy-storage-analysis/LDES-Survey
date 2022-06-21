#%%
import os
import pandas as pd
import json
import es_utils
#PDF location info
pdf_folder = r'C:\Users\aspit\OneDrive\Literature\Zotero\Energy Storage'
pdf_fn =  r"Antunez_2018_Modelling and development of thermo-mechanical energy storage.pdf"
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
    extract_settings[i]['camelot_kwargs'].update({'flavor': DEFAULT_FLAVOR})
#%%

dfs = es_utils.pdf.extract_dfs(pdf_path, extract_settings)
#%%

#Setup table dictionary and do any processing here. 

tables = {}

tables = {'table_{}'.format(i+1): dfs[i] for i in range(len(dfs))}

#%%


#I am not sure why the extraction is picking up the caption, but this gets rid of it. 
# tables['table_1'] = tables['table_1'].loc[0:15]

tables['table_1'].columns = [c.replace('(cid:0)', '(') for c in tables['table_1'].columns]

# %%

output_folder = 'tables'
if not os.path.exists(output_folder): os.mkdir(output_folder)

for fn in os.listdir(output_folder):
    os.remove(os.path.join(output_folder, fn))

for table in tables:
    tables[table].to_csv('{}/{}.csv'.format(output_folder, table), index=False)
# %%
