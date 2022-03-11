#%%
import os
from matplotlib.pyplot import table
import pandas as pd
import json
import sys


import es_utils

# pdf_folder = r'/media/lee/Shared Storage/table_extract_text'

pdf_folder = r'C:\Users\aspit\OneDrive\Literature\Zotero\Energy Storage'
pdf_path = os.path.join(pdf_folder,r"Gur_2018_Review of electrical energy storage technologies, materials and systems.pdf")

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

table_settings = [{'template' : template} for template in templates]

dfs = es_utils.extract_dfs(pdf_path, extract_settings)

dfs[0]


# %%

output_folder = 'tables'

if not os.path.exists(output_folder): os.mkdir(output_folder)

for fn in os.listdir(output_folder):
    os.remove(os.path.join(output_folder, fn))

for i, df in enumerate(dfs):
    output_path = os.path.join(output_folder, 'table_{}.csv'.format(i+1))
    df.to_csv(output_path)
# %%
