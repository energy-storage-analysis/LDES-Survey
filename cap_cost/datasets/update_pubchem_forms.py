"""Updates the pubchem formulas in the chem lookup tables"""

#%%
import os
from os.path import join as pjoin
import numpy as np
import pandas as pd
from sympy import O



dataset_folder = '.'
dataset_index = pd.read_csv(pjoin(dataset_folder,'dataset_index.csv'), index_col=0)
pubchem_lookup = pd.read_csv(pjoin(dataset_folder, 'pubchem_lookup.csv'), index_col=0)

mat_names = []

for source, row in dataset_index.iterrows():

    fp = os.path.join(dataset_folder, row['price_data_path'])

    #TODO: add source forlder in index
    output_folder = os.path.split(fp)[0]
    source_folder = os.path.split(output_folder)[0]
    fp_mat_lookup = os.path.join(source_folder,'mat_lookup.csv')
    if os.path.exists(fp_mat_lookup):
        mat_lookup = pd.read_csv(fp_mat_lookup, index_col=0)
        mat_names = mat_lookup['material_name']
        pubchem_formulas = [pubchem_lookup.loc[mat_name]['pubchem_top_formula'] if mat_name in pubchem_lookup.index else np.nan for mat_name in mat_names]
        mat_lookup['pubchem_formula'] = pubchem_formulas
        mat_lookup.to_csv(fp_mat_lookup)

# %%
