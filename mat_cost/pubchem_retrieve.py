#%%
import sys
import pandas as pd
from os.path import join as pjoin
import numpy as np


df_singlemat = pd.read_csv('data/df_singlemat.csv', index_col=0)

#%%k



chemical_list = list(set(df_singlemat['material_name'].dropna()))
chemical_list
# %%

df_pubchem_existing = pd.read_csv('data/pubchem_lookup.csv', index_col=0)
df_pubchem_existing.index = df_pubchem_existing.index.str.lower()
df_pubchem_existing

# %%
missing_chemicals = [c for c in chemical_list if not c in df_pubchem_existing.index]
missing_chemicals 
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

for chem in tqdm(missing_chemicals):
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
    index = missing_chemicals,
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

df_out = pd.concat([
    df_pubchem_existing,
    df_chem
])
df_out

#%%

#I thnk this is not necessary anymore If I am only using pubchem? which returns normalized formulas


from es_utils.chem import mat2vec_process


#TODO: lowercase original pubchem lookup
df_out = df_out.reset_index()
df_out['index'] = df_out['index'].str.lower()
df_out = df_out.drop_duplicates(subset=['index'])
df_out = df_out.set_index('index')

pubchem_forms = df_out['pubchem_top_formula'].astype(str).apply(mat2vec_process)
pubchem_forms = pubchem_forms.replace('nan', np.nan)
pubchem_forms

#%%

pubchem_forms.where(pubchem_forms.duplicated(False)).dropna().sort_values()


#%%

df_out['pubchem_top_formula'] = pubchem_forms
df_out.index.name = 'material_name'

#%%

df_out.to_csv('data/pubchem_lookup.csv')
# %%
