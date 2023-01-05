
"""
Generates markdown tables from the collected csv files
"""

#%%
import os
from os.path import join as pjoin
import pandas as pd
from es_utils.units import prep_df_pint_out, read_pint_df

from pytablewriter import MarkdownTableWriter

output_folder = 'md_generated'
if not os.path.exists(output_folder): os.mkdir(output_folder)


from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')
input_dir = os.path.join(REPO_DIR, 'cap_cost','source_meta','tables')

#%%


individual_tables_dir = os.path.join(input_dir, 'individual')
fns = os.listdir(individual_tables_dir)

tables_text = ""

for fn in fns:

    df_sel = read_pint_df(os.path.join(individual_tables_dir, fn), index_col=[0,1])

    # df_sel = df_sel.pint.dequantify()

    SM_type = os.path.splitext(fn)[0]

    for col in df_sel.columns:
        # if col[1] != 'N/U':
        # if df_sel[col].dtype != 'object':
        if 'pint' in str(df_sel[col].dtype):
            df_sel[col] = df_sel[col].pint.quantity
            df_sel[col] = df_sel[col].round(2)

    writer = MarkdownTableWriter(dataframe=df_sel.reset_index())


    tables_text = tables_text + "## {}".format(SM_type) + '\n\n'
    tables_text = tables_text + writer.dumps()
    tables_text = tables_text + "\n\n"


with open(os.path.join(output_folder,'SM_type_tables.md'.format(SM_type)), 'w', encoding='utf-8') as f:
    f.write(tables_text)



df = pd.read_csv(pjoin(input_dir,'SM_type_source_counts.csv'))

#TODO: come up with some sort of long name (and units) system for displayed tables
df['SM_type'] = df['SM_type'].str.replace('_', ' ')
df['SM_type'] = df['SM_type'].str.replace('thermochemical', 'thermo-chemical')
df['sub_type'] = df['sub_type'].str.replace('_', ' ')
df.columns = [c.replace('_',' ') for c in df.columns]

df = df.rename({'0': 'Source Counts'})

writer = MarkdownTableWriter(dataframe=df)

with open(os.path.join(output_folder,'SM_type_source_counts.md'), 'w', encoding='utf-8') as f:
    f.write(writer.dumps())
    f.write(": Counts of each source's contribution to storage media of each type, sub-type, and material type.")


fp = os.path.join(REPO_DIR, r'cap_cost\source_meta\tables\SM_viable.csv')

df = read_pint_df(fp)

#TODO: come up with some sort of long name (and units) system for displayed tables
df['SM_type'] = df['SM_type'].str.replace('_', ' ')
df['SM_type'] = df['SM_type'].str.replace('thermochemical', 'thermo-chemical')
df.columns = [c.replace('_',' ') for c in df.columns]

df = df.drop('price sources', axis=1)
df = df.drop('SM sources', axis=1)

df = prep_df_pint_out(df)
df = df.reset_index()

df['C kwh'] = df['C kwh'].round(5)
df['specific price'] = df['specific price'].round(5)
df['specific energy'] = df['specific energy'].round(5)

# split out unit row 
new_cols = df.columns.droplevel(1)
df_col_row = pd.DataFrame(df.columns.droplevel().values.reshape(-1,len(df.columns)), columns = new_cols)
df.columns = new_cols
df = pd.concat([df_col_row, df])

writer = MarkdownTableWriter(dataframe=df)

with open(os.path.join(output_folder,'SM_viable.md'), 'w', encoding='utf-8') as f:
    f.write(writer.dumps())
    f.write(": Storage Media with $C_{kWh}$ < 10 USD/kWh, sorted by $C_{kWh}$")



#%%

# Various publicaiton material data

fp = os.path.join(REPO_DIR, r'cap_cost\datasets\pub\various_pub\output\mat_data.csv')

df = read_pint_df(fp)

df = prep_df_pint_out(df)
df = df.reset_index()

df = df[['index','original_name','source','notes']]

df.columns = df.columns.droplevel(1) # No units needed

writer = MarkdownTableWriter(dataframe=df)

with open(os.path.join(output_folder,'various_pub_mat_data.md'), 'w', encoding='utf-8') as f:
    f.write(writer.dumps())
    f.write(": Various publicaiton material data sources")


#%%


# Various publicaiton Storage medium data

fp = os.path.join(REPO_DIR, r'cap_cost\datasets\pub\various_pub\output\SM_data.csv')

df = read_pint_df(fp)

df = prep_df_pint_out(df)
df = df.reset_index()

df = df[['SM_name','SM_type','sub_type','source','notes']]

df.columns = df.columns.droplevel(1) # No units needed

writer = MarkdownTableWriter(dataframe=df)

with open(os.path.join(output_folder,'various_pub_SM_data.md'), 'w', encoding='utf-8') as f:
    f.write(writer.dumps())
    f.write(": Various publicaiton storage media")


#%%


# Various website material data

fp = os.path.join(REPO_DIR, r'cap_cost\datasets\web\various_web\output\mat_data.csv')

df = read_pint_df(fp)

df = prep_df_pint_out(df)
df = df.reset_index()

df = df[['index','original_name','source','notes']]

df.columns = df.columns.droplevel(1) # No units needed

writer = MarkdownTableWriter(dataframe=df)

with open(os.path.join(output_folder,'various_web_mat_data.md'), 'w', encoding='utf-8') as f:
    f.write(writer.dumps())
    f.write(": Various website material data sources")


#%%

fp = os.path.join(REPO_DIR, r'cap_cost\source_meta\tables\mat_data_vol.csv')
df = pd.read_csv(fp)

df = df[['index','vol_price', 'sources']]

df = df.rename({'vol_price': 'Volumetric Price $(USD/m^3)$'}, axis=1)

writer = MarkdownTableWriter(dataframe=df)

with open(os.path.join(output_folder,'mat_data_vol.md'), 'w', encoding='utf-8') as f:
    f.write(writer.dumps())
    f.write(": Volumetric Material cost datapoints")