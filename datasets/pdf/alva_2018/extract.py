#%%
import os
from matplotlib.pyplot import table
import pandas as pd
import camelot
import json
import sys
import numpy as np

sys.path.append('..')
import pdf_utils

# pdf_folder = r'/media/lee/Shared Storage/table_extract_text'
pdf_folder = r'C:\Users\aspit\OneDrive\Literature\Zotero\Energy Storage'
pdf_path = os.path.join(pdf_folder, r"Alva et al_2018_An overview of thermal energy storage systems.pdf")

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

dfs = pdf_utils.extract_dfs(pdf_path, extract_settings)

dfs[0]

tables = {}
#%%
table8_items = [7,8,9,10]
dfs_table8 = [dfs[i] for i in table8_items]

dfs_table8[1].columns = dfs_table8[0].columns
dfs_table8[2].columns = dfs_table8[0].columns
dfs_table8[3].columns = dfs_table8[0].columns

df_table8 = pd.concat(dfs_table8)
df_table8 = df_table8.reset_index(drop=True)

df_table8 = df_table8.rename(
    {'Type  ': 'type',
       'Class  ': 'class', 
       'Thermal storage material  ': 'original_name',
       'Phase change temperature (degC) ': 'phase_change_T',
       'Latent heat (kJ$kg\n-1) ': 'sp_latent_heat',
       '-3)\nDensity (kg$m  ': 'density',
       'Thermal conductivity (W$m\n-1 K\n-1)': 'kth',
       'Latent heat storage capacity (MJ$m\n-3) ': 'vol_latent_heat',
       'Technical grade cost ($$kg\n-1) ': 'cost',
       'Remarks  ':'remarks'},
axis=1)

df_table8 = df_table8.drop('type',axis=1)
df_table8 = df_table8.drop('remarks',axis=1)

df_table8['phase_change_T'] = df_table8['phase_change_T'].replace('40-45', '42.5')
df_table8['phase_change_T'] = df_table8['phase_change_T'].replace('',np.nan).astype(float)

df_table8['sp_latent_heat'] = df_table8['sp_latent_heat'].replace('',np.nan).astype(float)
df_table8['sp_latent_heat'] = df_table8['sp_latent_heat']/3600

df_table8['class'] = df_table8['class'].replace('',np.nan).fillna(method='ffill') 
df_table8['class'] = df_table8['class'].replace('eutectics', 'Organic', regex=True)
df_table8['class'] = df_table8['class'].replace('Organic', 'Organic Eutectic', regex=True)
df_table8['class'] = df_table8['class'].replace('Inorganic ', '', regex=True)
df_table8['cost'] = df_table8['cost'].replace('',np.nan).dropna().replace('\(RG\)','', regex=True).astype(float)

tables['table_8'] = df_table8

#%%
df_table4 = dfs[3].replace('',np.nan)

df_table4.columns = [c.strip() for c in df_table4.columns]
df_table4 = df_table4.dropna(subset=['Property']).set_index('Property')
df_table4 = df_table4.T
df_table4 = df_table4.iloc[2:]



df_table4['class'] = 'Thermal Oils'
df_table4 = df_table4.rename({  
    '-1 degC\n-1)\nSpeciﬁc heat capacity at 210 degC (kJ kg': 'Cp',
    'Thermal conductivity at 210 degC (W m\n-1 K\n-1)': 'kth',
    'Cost (V$t\n-1)': 'cost'
    }, axis=1)
df_table4.index.name = 'original_name'

df_table4['cost'] = df_table4['cost'].str.replace(',','')
df_table4['cost'] = df_table4['cost'].replace('e','nan')
df_table4['cost'] = df_table4['cost'].astype(float)
df_table4['cost'] = df_table4['cost']*(1/1000) #euro/ton to dollar/kg (roughly)


df_table4.index = df_table4.index.str.replace("®", '', regex=True)
df_table4.index = df_table4.index.str.replace("\\n", ' ', regex=True)
df_table4.index = df_table4.index.str.strip()

tables['table_4'] = df_table4


df_table5 = dfs[4]

df_table5.columns = [c.strip() for c in df_table5.columns]
# df_table5.columns = df_table5.columns.str.replace(r'\r\n',r'\n', regex=True)

df_table5 = df_table5.dropna(subset=['Highest operating temperature (degC)'])
df_table5['class'] = 'Molten Salt'

df_table5 = df_table5.rename({
    'Salt/eutectic': 'original_name',
    'Speciﬁc heat (kJ$kg\n-1 degC\n-1)': 'Cp',
    'Thermal conductivity (W$m\n-1 K\n-1)': 'kth',
    'Cost ($$kg\n-1)': 'cost'
    }, axis=1)


df_table5['original_name'] = df_table5['original_name'].replace('e','-')
df_table5 = df_table5.set_index('original_name')
df_table5['cost'] = df_table5['cost'].replace('e','nan')

df_table5 = df_table5.iloc[[0,2,4]]


# df_table5 = df_table5.drop('LiNO3')
tables['table_5'] = df_table5


df_table6 = dfs[5]
df_table6.columns = [c.strip() for c in df_table6.columns]
# df_table6.columns = df_table6.columns.str.replace(r'\r\n',r'\n', regex=True)

df_table6['class'] = 'Metal Alloy'
df_table6 = df_table6.rename({
    'Metal/Alloy': 'original_name',
    'Speciﬁc heat -1\nkJ$kg\n-1 degC': 'Cp',
    'Thermal conductivity (W$m\n-1 K\n-1)' : 'kth',
    'Cost ($$kg\n-1)': 'cost'
    }, axis=1)

df_table6 = df_table6.set_index('original_name')
tables['table_6'] = df_table6

df_table7 = dfs[6]

df_table7.columns = [c.strip() for c in df_table7.columns]
df_table7 = df_table7.dropna(subset=['Type'])
df_table7['class'] = 'Rocks'
# df_table7['cost'] = 0.1
df_table7['cost'] = np.nan
# df_table7.columns = df_table7.columns.str.replace(r'\r\n',r'\n', regex=True)

df_table7 = df_table7.rename({
    'Rock': 'original_name',
    'Speciﬁc heat (kJ$kg\n-1 degC\n-1) @20 degC': 'Cp',
    'Thermal conductivity (W$m\n-1 K\n-1)': 'kth',
    }, axis=1)

df_table7 = df_table7.set_index('original_name')

from pdf_utils import average_range
df_table7['Cp'] = df_table7['Cp'].apply(average_range)

tables['table_7'] = df_table7 

# %%

table
#%%

output_folder = 'tables'
if not os.path.exists(output_folder): os.mkdir(output_folder)

for fn in os.listdir(output_folder):
    os.remove(os.path.join(output_folder, fn))

for table in tables:
    tables[table].to_csv('{}/{}.csv'.format(output_folder, table))
# %%
