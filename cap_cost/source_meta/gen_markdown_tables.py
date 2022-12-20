
"""
Generates markdown tables from the collected csv files
"""

#%%
import os
from os.path import join as pjoin
import pandas as pd
from es_utils.units import prep_df_pint_out, read_pint_df


#%%

input_dir = 'tables/individual'
fns = os.listdir(input_dir)

from pytablewriter import MarkdownTableWriter

tables_text = ""

for fn in fns:

    df_sel = read_pint_df(os.path.join(input_dir, fn), index_col=[0,1])

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


with open(os.path.join('docs','SM_type_tables.md'.format(SM_type)), 'w', encoding='utf-8') as f:
    f.write(tables_text)





SM_source_info = pd.read_csv(pjoin('tables','SM_type_source_counts.csv'), index_col=0)

writer = MarkdownTableWriter(dataframe=SM_source_info.reset_index())

with open(os.path.join('docs','SM_type_source_counts.md'), 'w', encoding='utf-8') as f:
    f.write(writer.dumps())



