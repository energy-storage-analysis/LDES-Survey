#%%
import os
from matplotlib.pyplot import table
import pandas as pd
import json
import sys

sys.path.append('..')
import pdf_utils

pdf_folder = r'/media/lee/Shared Storage/table_extract_text'
pdf_path = os.path.join(pdf_folder,r"Gur_2018_Review of electrical energy storage technologies, materials and systems.pdf")

template_path = 'tabula_template.json'
with open(template_path, 'r') as f:
    templates= json.load(f)

#%%

table_settings = [{'template' : template} for template in templates]

dfs = pdf_utils.extract_dfs(pdf_path, table_settings)

dfs[0]


# %%

output_folder = 'output'

for fn in os.listdir(output_folder):
    os.remove(os.path.join(output_folder, fn))

for i, df in enumerate(dfs):
    output_path = os.path.join(output_folder, 'table_{}.csv'.format(i+1))
    df.to_csv(output_path)
# %%
