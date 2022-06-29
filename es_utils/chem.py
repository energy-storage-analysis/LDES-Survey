import numpy as np
import pandas as pd
import re

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





def process_chem_lookup(chem_lookup):

    chem_lookup['molecular_formula_norm'] = chem_lookup['molecular_formula'].apply(pymatgen_process)

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




def calculate_formula_price(chemparse_dict, element_prices):
    total_price = 0
    total_mass = 0
    for atom, num in chemparse_dict.items():
        if atom in element_prices.index:

            row = element_prices.loc[atom]
            
            kg_per_mol = row['molar_mass']/1000

            total_mass += kg_per_mol*num #kg/mol

            cost_per_mol = row['cost']*kg_per_mol
            total_price += cost_per_mol*num   #$/mol 
        else:
            return np.nan

    price = total_price/total_mass #$/kg

    return price


def normalize_list(l_str):
    l = l_str.strip('][').split(', ')
    list_out = []
    for f in l:
        list_out.append(normalize_formula(f)[0])
    list_out = str(list_out)
    return list_out

## Custom functions from mat2vec. 

from monty.fractions import gcd_float
from pymatgen.core.composition import CompositionError, Composition

def get_ordered_integer_formula(el_amt, max_denominator=1000):
    """Converts a mapping of {element: stoichiometric value} to a alphabetically ordered string.

    Given a dictionary of {element : stoichiometric value, ..}, returns 
    1)a string with elements ordered alphabetically and stoichiometric values normalized to smallest common
    integer denominator
    2) the greatest common denominator used  

    Args:
        el_amt: {element: stoichiometric value} mapping.
        max_denominator: The maximum common denominator of stoichiometric values to use for
            normalization. Smaller stoichiometric fractions will be converted to the same
            integer stoichiometry.

    Returns:
        A material formula string with elements ordered alphabetically and the stoichiometry
        normalized to the smallest integer fractions.

    """
    gcd = gcd_float(list(el_amt.values()), 1 / max_denominator)
    d = {k: round(v / gcd) for k, v in el_amt.items()}
    formula = ""
    for k in sorted(d):
        if d[k] > 1:
            formula += k + str(d[k])
        elif d[k] != 0:
            formula += k
    return formula, gcd

def normalize_formula(formula, max_denominator=1000):
    """Normalizes chemical formula to smallest common integer denominator, and orders elements alphabetically.

    Args:
        formula: the string formula.
        max_denominator: highest precision for the denominator (1000 by default).

    Returns:
        A normalized formula string, e.g. Ni0.5Fe0.5 -> FeNi.
    """
    try:
        formula_dict = Composition(formula).get_el_amt_dict()
        norm_formula, gcd = get_ordered_integer_formula(formula_dict, max_denominator)
        return norm_formula, gcd 
    except (CompositionError, ValueError):
        #Happens if string does not match formula
        return formula, 1

def pymatgen_process(f):
    if f != f:
        return np.nan
    f = str(f)
    s, gcd = normalize_formula(f)
    return s


def calc_hydrate_factor(anhydrous_formula, hydrate_count):
    """Calculates the mass ratio (hydrated/anhydrous) to scale specific price"""

    mu_anhydrous = get_molecular_mass(anhydrous_formula)
    # mu_water = get_molecular_mass('H2O')*hydrate_count
    mu_hydrate = 18.015*hydrate_count

    price_factor = (mu_anhydrous+mu_hydrate)/mu_anhydrous
    return price_factor



def format_chem_formula(s):
    """
    This function is a set of sequential regex replacements to try and format the chemical formula style names in the material index
    In general this is hacky and probably could be simplified. The names are pftem not just simply chemical formulas which means pyvalem cannot be used. 
    """
    s = re.sub(r'([a-zA-Z)])(\d\.\d+)(\D|$)',r'\1_{\2}\3', s, count=5)

    #TODO: I cannot seem to get the end of line character to behave correctly in a regex OR statement
    s = re.sub(r'([a-zA-Z)](?!_))(\d\d?)(\D)',r'\1_{\2}\3', s, count=5)
    s = re.sub(r'([a-zA-Z)](?!_))(\d\d?)$',r'\1_{\2}', s, count=5)

    #TODO: there are some remaining formula segments (e.g. V_2O5) that don't seem to get caught and I don't know why 
    s  = re.sub(r'(\d)([a-zA-Z])(\d)', r'\1\2_\3',s)

    s = s.replace(" ", "\ ", -1)
    return s