"""Updates the pubchem lookup table for all materials found (used before update_pubchem_forms.py)"""
#%%
import sys
import pandas as pd
from os.path import join as pjoin
import numpy as np
import os

dataset_folder = '.'
dataset_index = pd.read_csv(pjoin(dataset_folder,'dataset_index.csv'), index_col=0)

mat_names = []

for source, row in dataset_index.iterrows():

    fp = os.path.join(dataset_folder, row['price_data_path'])

    #TODO: add source forlder in index
    output_folder = os.path.split(fp)[0]
    source_folder = os.path.split(output_folder)[0]
    fp_mat_lookup = os.path.join(source_folder,'mat_lookup.csv')
    if os.path.exists(fp_mat_lookup):
        mat_names_source = pd.read_csv(fp_mat_lookup)['material_name'].dropna().values
        mat_names.extend(mat_names_source)


mat_names = list(set(mat_names))

# %%
import os

fp_pubchem_lookup = 'pubchem_lookup.csv'
if os.path.exists(fp_pubchem_lookup):
    df_pubchem_existing = pd.read_csv(fp_pubchem_lookup, index_col=0)
    # df_pubchem_existing.index = df_pubchem_existing.index.str.lower()
    missing_materials = [c for c in mat_names if not c in df_pubchem_existing.index]
    mat_search_list = missing_materials
else:
    df_pubchem_existing = None
    mat_search_list = mat_names


# mat_search_list = mat_search_list[0:4]
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

for chem in tqdm(mat_search_list):
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

#%%

df_chem = pd.DataFrame(
    {'pubchem_formulas': pubchem_output},
    index = mat_search_list,
)

df_chem

#%%



from es_utils.chem import get_top_formula

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
df_chem['pubchem_top_formula'] = [f if f != None else np.nan for f in df_chem['pubchem_top_formula']]
df_chem
# df_chem['pubchem_top_formula'].values
#%%


if type(df_pubchem_existing) == type(None):
    df_out = df_chem
else:
    df_out = pd.concat([
        df_pubchem_existing,
        df_chem
    ])

#%%

#I thnk this is not necessary anymore If I am only using pubchem? which returns normalized formulas


from es_utils.chem import pymatgen_process


#TODO: lowercase original pubchem lookup
df_out = df_out.reset_index()
# df_out['index'] = df_out['index'].str.lower()
df_out = df_out.drop_duplicates(subset=['index'])
df_out = df_out.set_index('index')

pubchem_forms = df_out['pubchem_top_formula'].astype(str).apply(pymatgen_process)
pubchem_forms = pubchem_forms.replace('nan', np.nan)
pubchem_forms

#%%

pubchem_forms.where(pubchem_forms.duplicated(False)).dropna().sort_values()


#%%

df_out['pubchem_top_formula'] = pubchem_forms
df_out.index.name = 'material_name'

#%%

df_out.to_csv('pubchem_lookup.csv')
# %%
