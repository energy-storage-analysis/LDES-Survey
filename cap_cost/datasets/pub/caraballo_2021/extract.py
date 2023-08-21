#%%
import os
import pandas as pd
import json
import es_utils

#PDF location info
from dotenv import load_dotenv
load_dotenv()

pdf_folder = os.getenv('PDF_FOLDER_PATH')
pdf_fn =  r"Caraballo et al_2021_Molten Salts for Sensible Thermal Energy Storage.pdf"
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

# tables = {'table_{}'.format(i+1): dfs[i] for i in range(len(dfs))}

dfs[0]['sub_type'] = 'Nitrate'
# dfs[4]['type'] = 'Nitrate'
# dfs[8]['type'] = 'Nitrate'
dfs[1]['sub_type'] = 'Chloride'
# dfs[5]['type'] = 'Chloride'
# dfs[9]['type'] = 'Chloride'
dfs[2]['sub_type'] = 'Fluoride'
# dfs[6]['type'] = 'Fluroide'
# dfs[10]['type'] = 'Fluoride'
dfs[3]['sub_type'] = 'Carbonate'
# dfs[7]['type'] = 'Carbonate'
# dfs[11]['type'] = 'Carbonate'

tables['table_1'] = pd.concat([
    dfs[0],
    dfs[1],
    dfs[2],
    dfs[3],
])

tables['table_2'] = pd.concat([
    dfs[4],
    dfs[5],
    dfs[6],
    dfs[7],
])

tables['table_3'] = pd.concat([
    dfs[8],
    dfs[9],
    dfs[10],
    dfs[11],
])

tables['table_1'].columns = ['name','composition', 'T_melt','T_max', 'ref', 'sub_type']
tables['table_2'].columns = ['name','mass_density', 'Cp','ref']
tables['table_3'].columns = ['name','specific_price_orig', 'specific_energy_orig','volumetric_energy_orig','C_kwh_orig','ref']

for table in tables:
    tables[table] = tables[table].reset_index(drop=True)

tables['table_1']['composition'] = tables['table_1']['composition'].str.replace('–', '-', regex=False)
tables['table_2']['mass_density'] = tables['table_2']['mass_density'].str.replace('−', '-', regex=False)
tables['table_2']['Cp'] = tables['table_2']['Cp'].str.replace('−', '-', regex=False)

# %%

output_folder = 'tables'
if not os.path.exists(output_folder): os.mkdir(output_folder)

for fn in os.listdir(output_folder):
    os.remove(os.path.join(output_folder, fn))

for table in tables:
    tables[table].to_csv('{}/{}.csv'.format(output_folder, table), index=False)
# %%
