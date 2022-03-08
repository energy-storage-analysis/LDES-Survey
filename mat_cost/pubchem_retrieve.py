#%%
import sys
import pandas as pd
from os.path import join as pjoin
import numpy as np

dataset_folder = '../datasets'


datasets = [
    pjoin(dataset_folder, 'ISE/output/processed.csv'),
    pjoin(dataset_folder, 'usgs/output/processed.csv'),
    pjoin(dataset_folder, 'pdf/li_2017/output/process.csv'),
    pjoin(dataset_folder, 'pdf/alva_2018/output/sensible.csv'),
]

chemical_list = []

for dataset in datasets:
    chemical_list.extend(pd.read_csv(dataset)['material_name'].dropna().values)

chemical_list = list(set(chemical_list))
# %%

# %%


chems = chemical_list#[0:5]
chems
#%%


from tqdm import tqdm
import time


import pubchempy as pcp
from chemspipy import ChemSpider

from dotenv import load_dotenv
load_dotenv()



from collections import Counter

print("Getting pubchem data")
pubchem_output = []

num_tries =10

for chem in tqdm(chems):
    tries = 0
    while True:
        if tries > num_tries:
            pubchem_output.append('HTTP Error')
            break
        try:
            results = pcp.get_substances(chem, 'name')

            comps = [r.standardized_compound for r in results if 'compound' in r.record]

            comps  = [c for c in comps if c != None]

            formulas = [c.to_dict()['molecular_formula'] for c in comps]

            formula_counts = dict(Counter(formulas))

            pubchem_output.append(formula_counts)

            break
        except pcp.PubChemHTTPError:
            print("HTTP Error")
            time.sleep(10)
            tries += 1
            continue

pubchem_output

# %%

# import os

# api_key = os.getenv('CHEMSPIDER_API')
# cs = ChemSpider(api_key)


# #%%
# print("getting chemspider data")

# chemspi_output = []

# for chem in tqdm(chems):
#     results = cs.search(chem)

#     formulas = []

#     for r in results:
#         formulas.append(r.molecular_formula)
        

#     formula_counts = dict(Counter(formulas))

#     chemspi_output.append(formula_counts)

# chemspi_output


#%%

df_chem = pd.DataFrame(
    {'pubchem_formulas': pubchem_output},
    # 'chemspi_output': chemspi_output},
    index = chems,
)

df_chem

#%%


sys.path.append('../datasets/pdf')
from pdf_utils import get_top_formula

import ast 
# df_chem['pubchem_formulas'] = df_chem['pubchem_formulas'].apply(ast.literal_eval)
df_chem['pubchem_top_formula'] = df_chem['pubchem_formulas'].apply(get_top_formula)

# df_chem['chemspi_output'] = df_chem['chemspi_output'].apply(ast.literal_eval)
# df_chem['chemspi_top_formula'] = df_chem['chemspi_output'].apply(get_top_formula)

# df_chem['chemspi_top_formula']  = df_chem['chemspi_top_formula'].str.replace('_','')
# df_chem['chemspi_top_formula']  = df_chem['chemspi_top_formula'].str.replace('{','', regex=True)
# df_chem['chemspi_top_formula']  = df_chem['chemspi_top_formula'].str.replace('}','', regex=True)

df_chem


#%%

df_chem.to_csv('data/pubchem_lookup.csv')