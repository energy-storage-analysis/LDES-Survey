"""
This script combines together the readme files from different dataset folders
"""


import pandas as pd
import os
import re
from collections import Counter

from es_utils.units import read_pint_df

dataset_index = pd.read_csv('dataset_index.csv', index_col=0)


def get_source_SM_counts(df):
    counts = Counter(df)
    counts = str(dict(counts))
    return counts

# SM_source_info = df_SM.groupby('source')['SM_type'].apply(get_source_SM_counts).dropna()
# SM_source_info.name = 'SM types'

# price_source_info = df_mat_data.groupby('source').apply(len)
# price_source_info.name = 'num prices'

# source_info = pd.concat([SM_source_info, price_source_info],axis=1 )

# source_info = source_info.sort_index()

# source_info['num prices'] = source_info['num prices'].fillna(0).astype(int).astype(str).str.replace('^0$','-',regex=True)
# source_info['SM types'] = source_info['SM types'].fillna('-')


with open('README_combined.md', 'w', encoding='utf-8') as f:
    for source, row in dataset_index.iterrows():

        f.write("\n\n## {}\n".format(source))

        fp= os.path.join(row['folder'], 'README.md')
        if os.path.exists(fp):
            with open(fp,'r', encoding='utf-8') as f_read:
                r_text = f_read.read()
            
            #Remove any text after the 'Development' header
            r_text = re.sub(r"## Development[\S\n\t\v ]*", '', r_text)

            r_text = re.sub(r"#",r"##", r_text)

            f.write(r_text)

        else:
            f.write("No Readme file found")

        
        # f.write("\n### Source Material and Storage media info")
        f.write("\n")
        
        fp_mat_data = os.path.join(row['folder'], 'output','mat_data.csv')
        if os.path.exists(fp_mat_data):
            df_mat_data = read_pint_df(fp_mat_data)

            f.write("\nNumber of prices: {}".format(len(df_mat_data)))
            
        fp_SM_data = os.path.join(row['folder'], 'output','SM_data.csv')
        if os.path.exists(fp_SM_data):
            df_SM_data = read_pint_df(fp_SM_data)

            count_dict = dict(Counter(df_SM_data['SM_type']))
            f.write("\n\n Types of storage media - ")
            for key, val in count_dict.items():
                key = key.replace("_"," ").capitalize()
                f.write("{}: {}, ".format(key, val))
            

        f.write("\n")


os.system("pandoc -o README_combined.docx -f markdown -t docx README_combined.md")