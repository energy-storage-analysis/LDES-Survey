#%%
import os
from matplotlib.pyplot import table
import pandas as pd
import camelot
import json
import sys


import es_utils

# pdf_folder = r'/media/lee/Shared Storage/table_extract_text'
pdf_folder = r'C:\Users\aspit\OneDrive\Literature\Zotero\Energy Storage'
pdf_path = os.path.join(pdf_folder, r"Kim et al_2013_Liquid Metal Batteries.pdf")

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
tables = {'table_{}'.format(i+1): dfs[i] for i in range(len(dfs))}

#%%

tables['table_3'] = tables['table_3'].set_index('B')
tables['table_3'].index.name = 'partner_metal'

tables['table_3'] = tables['table_3'].replace('−','-',regex=True)
tables['table_3'] = tables['table_3'].replace("(\d\.\d\d-\d\.\d\d).+",r'\1',regex=True )
tables['table_3']
#%%

tables['table_4'].columns = ['metal', 'molar_price','std_dev_pct']


#Some metals have an 'a' superscript
tables['table_4']['metal'] = tables['table_4']['metal'].str.replace('aa','a')
tables['table_4']['metal'] = tables['table_4']['metal'].str.replace('Ka','K')
tables['table_4']['metal'] = tables['table_4']['metal'].str.replace('Mga','Mg')
tables['table_4']['metal'] = tables['table_4']['metal'].str.replace('Tla','Tl')

tables['table_4'] = tables['table_4'].set_index('metal')

tables['table_4']

# %%

output_folder = 'tables'
if not os.path.exists(output_folder): os.mkdir(output_folder)

for fn in os.listdir(output_folder):
    os.remove(os.path.join(output_folder, fn))

for table in tables:
    tables[table].to_csv('{}/{}.csv'.format(output_folder, table))
# %%
