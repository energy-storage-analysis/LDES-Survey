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