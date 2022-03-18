#%%
import os
from matplotlib.pyplot import table
import pandas as pd
import camelot
import json
import sys
import numpy as np


import es_utils

# pdf_folder = r'/media/lee/Shared Storage/table_extract_text'
pdf_folder = r'C:\Users\aspit\OneDrive\Literature\Zotero\Energy Storage'
pdf_path = os.path.join(pdf_folder, r"Choi_Yoon_2015_Nanostructured Electrode Materials for Electrochemical Capacitor Applications.pdf")

template_path = 'tabula_template.json'
with open(template_path, 'r') as f:
    templates= json.load(f)

template_path = 'extract_settings.json'
with open(template_path, 'r') as f:
    extract_settings= json.load(f)

for i in range(len(extract_settings)):
    extract_settings[i]['template'] = templates[i]
    extract_settings[i]['column_rows'] = 3

    if 'camelot_kwargs' not in extract_settings[i]: extract_settings[i]['camelot_kwargs'] = {}
    extract_settings[i]['camelot_kwargs'].update({'flavor': 'stream', 'row_tol':10})

#%%

dfs = es_utils.pdf.extract_dfs(pdf_path, extract_settings)

dfs[0]

tables = {}
#%%

tables['table_1'] = pd.concat([dfs[0], dfs[1]])
# tables['table_1a'] = dfs[0]
# tables['table_1b'] = dfs[1]
tables['table_2'] = dfs[2]
tables['table_3'] = dfs[3]

for table in tables:
    tables[table].columns = [c.strip().replace('−','-') for c in tables[table].columns]
    # for column in tables[table].columns:
    #     tables[table][column] = tables[table][column].str.replace('−','-',regex=False)


tables['table_3'] = tables['table_3'].rename({
    'Materials (1)': 'Materials',
    'Electrode System (2,3)': 'Electrode System (1,2)',
    'Specific capacitance (F·g-1)':'Specific Capacitance (F·g-1)'
}, axis=1)

#%%

output_folder = 'tables'
if not os.path.exists(output_folder): os.mkdir(output_folder)

for fn in os.listdir(output_folder):
    os.remove(os.path.join(output_folder, fn))

for table in tables:
    tables[table].to_csv('{}/{}.csv'.format(output_folder, table), index=False)
# %%
