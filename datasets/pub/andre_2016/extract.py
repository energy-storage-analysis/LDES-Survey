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
pdf_path = os.path.join(pdf_folder, r"André et al_2016_Screening of thermochemical systems based on solid-gas reversible reactions for.pdf")

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

dfs = es_utils.pdf.extract_dfs(pdf_path, extract_settings)

dfs[0]

tables = {}
#%%

for i in range(1,5):
    tables['table_{}'.format(i+1)] = dfs[i]
    
    
    
for table in tables:
    
    tables[table] = tables[table].rename({'Chemical material': 'chemical'}, axis=1)
    tables[table]['chemical'] = tables[table]['chemical'].replace('F-2O3/F-3O4', 'Fe2O3/Fe3O4')
    tables[table][['reactant','product']] = tables[table]['chemical'].str.split('/', expand=True)
    tables[table] = tables[table].drop('chemical', axis=1).set_index('reactant')



tables['table_2']
#%%


types = {
    'table_2': 'sulfates',
    'table_3': 'carbonates',
    'table_4': 'hydroxides',
    'table_5': 'oxides',
}
#Were just going to keep the SO2 +1/2O2 reaction, as they say it is more relevant, and the data are similar anyway. I think the difference is in whether you let the oxygen in/escape?
tables['table_2'] = tables['table_2'].iloc[:,3:]

# tables['table_2'] = tables['table_2'][['Chemical','Temperature.1','Reaction Enthalpy','Gravimetric Storage den-']]

columns = ['temperature','enthalpy','specific_energy','product']
for table in tables:
    # tables[table] = tables[table].iloc[1:] #remove the extra column information
    tables[table].columns = columns
    tables[table]['type'] = types[table]

#%%

tables['table_2']


#%%

output_folder = 'tables'
if not os.path.exists(output_folder): os.mkdir(output_folder)

for fn in os.listdir(output_folder):
    os.remove(os.path.join(output_folder, fn))

for table in tables:
    tables[table].to_csv('{}/{}.csv'.format(output_folder, table))
# %%
