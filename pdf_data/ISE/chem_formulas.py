#%%
import os
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv
load_dotenv()
import time

import pubchempy as pcp
from chemspipy import ChemSpider

df = pd.read_csv('output/ISE_proc_edit.csv', index_col=0)
df
#%%

from collections import Counter

chems = list(set(df['chemical']))
df_chem = pd.DataFrame(index=chems)

#%%

print("Getting pubchem data")
pubchem_output = []

for chem in tqdm(chems):
    time.sleep(10)
    try:
        results = pcp.get_substances(chem, 'name')

        comps = [r.standardized_compound for r in results if 'compound' in r.record]

        comps  = [c for c in comps if c != None]

        formulas = [c.to_dict()['molecular_formula'] for c in comps]

        formula_counts = dict(Counter(formulas))

        pubchem_output.append(formula_counts)

    except pcp.PubChemHTTPError:
        print("HTTP Error")
        pubchem_output.append('HTTP Error')

pubchem_output


#%%

df_chem['pubchem_formulas'] = pubchem_output
df_chem

# %%



api_key = os.getenv('CHEMSPIDER_API')
cs = ChemSpider(api_key)
# %%

#%%

print("getting chemspider data")

chemspi_output = []

for chem in tqdm(chems):
    results = cs.search(chem)

    formulas = []

    for r in results:
        formulas.append(r.molecular_formula)
        

    formula_counts = dict(Counter(formulas))

    chemspi_output.append(formula_counts)



# %%

df_chem['chemspi_output'] = chemspi_output
df_chem

#%%

df_chem.to_csv('output/ISE_chem_data.csv')