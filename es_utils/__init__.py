from . import chem, pdf

def extract_df_physprop(df, physprops):

    df_phyprop = df[['original_name',*physprops]].dropna(subset=physprops, how='all')

    return df_phyprop

def extract_df_price(df):
    df_prices = df.where(~df['specific_price'].isna()).dropna(subset=['specific_price'])
    df_prices = df_prices[['original_name','specific_price']]
    return df_prices


def join_col_vals(df_dup, column):
    "Joins together non nan values in a column into a string list"
    col_vals = df_dup[column].dropna()
    source_list = ", ".join(set(col_vals))
    return source_list