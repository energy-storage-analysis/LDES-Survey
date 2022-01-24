#%%
import os
from matplotlib.pyplot import table
import pandas as pd
import camelot
import json
import sys

sys.path.append('..')
import pdf_utils

pdf_folder = r'/media/lee/Shared Storage/table_extract_text'
pdf_path = os.path.join(pdf_folder,r"Gur_2018_Review of electrical energy storage technologies, materials and systems.pdf")

template_path = 'tabula_template.json'
with open(template_path, 'r') as f:
    templates= json.load(f)

pdf_width, pdf_height = pdf_utils.get_pdf_size(pdf_path, 1) #assumes all heights are same as page 1


#%%

table_settings = [{'template' : template} for template in templates]


dfs = []
for setting in table_settings:
    print("table on page {}".format(setting['template']['page']))
    template = setting['template']
    page = template['page']
    table_area = pdf_utils.extract_table_area(template, pdf_height)

    columns = setting['columns'] if 'columns' in setting else None
    try:
        tables = camelot.read_pdf(pdf_path, pages=str(page), table_areas= table_area, flavor='stream')

        df = tables[0].df

        df = df.replace(to_replace='e(\d)', value=r'-\1', regex=True)
        df = df.replace('\(cid:3\)', 'deg', regex=True)
        df = df.replace('\(cid:1\)', '-', regex=True)

        #Set first row as column for all, then concat for others. This keeps compatibility with tabula
        if 'column_rows' in setting:
            column_rows = setting['column_rows']

            df = pdf_utils.concat_row_to_columns(df, column_rows)

    except:
        print("Error, skipping and returning blank dataframe")
        df = pd.DataFrame()

    dfs.append(df)


dfs[0]

#%%

# %%

output_folder = 'output'

for fn in os.listdir(output_folder):
    os.remove(os.path.join(output_folder, fn))

for i, df in enumerate(dfs):
    output_path = os.path.join(output_folder, 'table_{}.csv'.format(i+1))
    df.to_csv(output_path)
# %%
