from . import chem, pdf



def extract_df_mat(df):
    df_prices = df.dropna(subset=['specific_price'])
    df_prices = df_prices[['original_name','molecular_formula','specific_price']]
    return df_prices


def join_col_vals(s_dup, make_set=True, sort=True):
    "Joins together non nan values in a column into a string list"
    col_vals = s_dup.dropna().values
    if make_set: col_vals = list(set(col_vals))
    if sort: col_vals = sorted(col_vals)
    col_vals = [str(c) for c in col_vals]
    source_list = ", ".join(col_vals)
    return source_list