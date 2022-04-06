from . import chem, pdf



def extract_df_mat(df):
    df_prices = df.where(~df['specific_price'].isna()).dropna(subset=['specific_price'])
    df_prices = df_prices[['original_name','molecular_formula','specific_price']]
    return df_prices


def join_col_vals(s_dup):
    "Joins together non nan values in a column into a string list"
    col_vals = s_dup.dropna()
    col_vals = sorted(list(set(col_vals)))
    source_list = ", ".join(col_vals)
    return source_list