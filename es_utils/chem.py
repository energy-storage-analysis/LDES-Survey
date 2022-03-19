import numpy as np
import pandas as pd

def get_top_formula(formula_dict):
    """
    Gets the top result of a dicionarly with counts as the value
    e.g. as a pubchem result
    """
    if len(formula_dict):
        t = pd.Series(formula_dict).sort_values(ascending=False).index[0]
        return t
    else:
        return None


#mtp is passed in as an instance to avoid loading mat2vec for all es_utils imports
def mat2vec_process(f, mtp):
    """
    Use mat2vec processor to normalize a chemical formula
    f: formula
    mtp: MaterialsTextProcessor instance

    TODO: mtp is overpowered for this application and should potentially be replaced with the component of mtp doing formula normalizations
    """
    if f != f:
        return np.nan
    f = str(f)
    s = mtp.process(f)[0][0]
    return s

def process_chem_lookup(chem_lookup, mtp=None):
    if mtp != None:
        if 'molecular_formula' in chem_lookup.columns:
            chem_lookup['molecular_formula'] = chem_lookup['molecular_formula'].apply(lambda x: mat2vec_process(x, mtp))

    index_values = []

    for i, row in chem_lookup.iterrows(): 
        index_use = row['index_use']
        if index_use == index_use:
            index_val = row[index_use]
        else:
            index_val = np.nan
        
        index_values.append(index_val)


    chem_lookup['index'] = index_values

    chem_lookup = chem_lookup.dropna(subset=['index'])
    return chem_lookup


from pyvalem.formula import Formula
import chemparse

def get_molecular_mass(f):
    if f == 'O2': #Assuming O2 means air...
        return 0
    if len(f) == 0:
        return np.nan

    element_dict = chemparse.parse_formula(f)
    
    total_mm = 0
    for element, amount in element_dict.items():
        element_mm = Formula(element).rmm
        total_mm += element_mm*amount

    return total_mm