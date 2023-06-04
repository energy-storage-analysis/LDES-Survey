"""
This script combines together the readme files from different dataset folders
"""


import pandas as pd
import os
import re
from collections import Counter
from pytablewriter import MarkdownTableWriter

from es_utils.units import read_pint_df


from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')
dataset_folder = os.path.join(REPO_DIR, 'cap_cost','datasets')

dataset_index = pd.read_csv(os.path.join(dataset_folder, 'dataset_index.csv'), index_col=0)
dataset_index[['first_level','second_level']] = dataset_index['folder'].str.split('\\', expand=True)

#For checking which storage media ended up in the final dataset (have enough physprop to calculate Ckwh)
df_final = read_pint_df(os.path.join(REPO_DIR, 'cap_cost/data_consolidated/SM_data.csv'), index_col=[0,1], drop_units=True)
df_final = df_final.dropna(subset=['C_kwh'])

def get_source_SM_counts(df):
    counts = Counter(df)
    counts = str(dict(counts))
    return counts

physical_property_lookup = pd.read_csv(os.path.join(REPO_DIR, 'cap_cost\data_consolidated\SM_column_info.csv'), index_col=0)

group_name_map = {
    'pub': 'Publications',
    'gov': 'Government Sources',
    'web': 'Web Sources',
    'manual': 'Manually Defined/Calculated',
}

output_folder = 'md_generated'
if not os.path.exists(output_folder): os.mkdir(output_folder)

with open(os.path.join(output_folder,'README_combined.md'), 'w', encoding='utf-8') as f:

    for group_name, df_subset in dataset_index.groupby('first_level'):

        if group_name in group_name_map:
            group_name = group_name_map[group_name]

        f.write("# {}\n".format(group_name))

        for source, row in df_subset.iterrows():

            # f.write("\n\n### {}\n".format(source))

            fp= os.path.join(dataset_folder, row['folder'], 'README.md')
            if os.path.exists(fp):
                with open(fp,'r', encoding='utf-8') as f_read:
                    r_text = f_read.read()
                
                #Remove any text after the 'Development' header
                r_text = re.sub(r"## Development[\S\n\t\v ]*", '', r_text)

                r_text = re.sub(r'(#+)', r'\1#', r_text)



                f.write(r_text)

            else:
                f.write("No Readme file found")

            
            # f.write("\n### Source Material and Storage media info")
            f.write("\n\n")

            writer = MarkdownTableWriter() 
            # writer.table_name = 'Source Data'
            writer.headers = ["Number Material Prices", "Storage media", "Physical Properties"]

            fp_mat_data = os.path.join(dataset_folder, row['folder'], 'output','mat_data.csv')
            if os.path.exists(fp_mat_data):
                df_mat_data = read_pint_df(fp_mat_data)
                n_prices_string = str(len(df_mat_data))
            else:
                n_prices_string = "None" 

                
            fp_SM_data = os.path.join(dataset_folder, row['folder'], 'output','SM_data.csv')
            if os.path.exists(fp_SM_data):
                df_SM_data = read_pint_df(fp_SM_data)
                df_SM_data = df_SM_data.set_index('SM_type', append=True) #Source SM data only is indexed by SM_name... 
                
                # For the storage media counts we are only including those that make it in the final dataset (can calculate Ckwh)
                df_SM_data_final = df_SM_data[df_SM_data.index.isin(df_final.index)]
                df_SM_data_final = df_SM_data_final.reset_index()
                count_dict = dict(Counter(df_SM_data_final['SM_type']))

                num_SM_string = "" 
                # f.write("\n\n Types of storage media - ")
                for key, val in count_dict.items():
                    key = key.replace("_"," ").capitalize()
                    num_SM_string = num_SM_string + "{}: {}, ".format(key, val)

                # For physical properties we include all data
                present_physprop = [prop for prop in physical_property_lookup.index if prop in df_SM_data.columns]
                physprop_str = ""
                for prop in present_physprop:
                    s_prop = df_SM_data[prop].dropna()
                    if len(s_prop):
                        physprop_symbol = "${}$".format(physical_property_lookup['symbol'][prop])
                        physprop_str = physprop_str + "{}: {}, ".format(physprop_symbol, len(s_prop))


            else:
                num_SM_string = 'None'
                physprop_str = "None"
                
            writer.value_matrix = [
                [n_prices_string,num_SM_string, physprop_str]
            ] 
            writer.stream = f
            writer.write_table()

            # f.write("\nNumber of prices: {}".format(len(df_mat_data)))

            f.write("\n")



            if source == 'Various pub':
                with open('md_generated/various_pub_mat_data.md') as f_read:
                    text = f_read.read()
                f.write("\n")
                f.write(text)
                f.write("\n\n")

                with open('md_generated/various_pub_SM_data.md') as f_read:
                    text = f_read.read()

                f.write(text)
                f.write("\n\n")

            if source == 'Various web':
                with open('md_generated/various_web_mat_data.md') as f_read:
                    text = f_read.read()

                f.write("\n")
                f.write(text)
                f.write("\n\n")
    # Convert to word document. 
