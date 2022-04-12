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
pdf_path = os.path.join(pdf_folder, r"Weinrich et al_2019_Silicon and Iron as Resource-Efficient Anode Materials for Ambient-Temperature.pdf")

template_path = 'tabula_template.json'
with open(template_path, 'r') as f:
    templates= json.load(f)

template_path = 'extract_settings.json'
with open(template_path, 'r') as f:
    extract_settings= json.load(f)

for i in range(len(extract_settings)):
    extract_settings[i]['template'] = templates[i]

    if 'camelot_kwargs' not in extract_settings[i]: extract_settings[i]['camelot_kwargs'] = {}
    extract_settings[i]['camelot_kwargs'].update({'flavor': 'stream', 'row_tol':7})

#%%

dfs = es_utils.pdf.extract_dfs(pdf_path, extract_settings)


tables = {'table_{}'.format(i+1): dfs[i] for i in range(len(dfs))}


#%%

tables['table_2'].columns = ['system', 'product','voltage','specific_energy','energy_density','performance','condition','ref_condition','cycles','ref_cycles']

tables['table_2']['system'] = tables['table_2']['system'].replace('',np.nan).fillna(method='ffill')

#%%

output_folder = 'tables'
if not os.path.exists(output_folder): os.mkdir(output_folder)

for fn in os.listdir(output_folder):
    os.remove(os.path.join(output_folder, fn))

for table in tables:
    tables[table].to_csv('{}/{}.csv'.format(output_folder, table), index=False)
# %%
