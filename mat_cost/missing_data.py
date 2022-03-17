#%%
import os
from os.path import join as pjoin
import numpy as np
import pandas as pd
from es_utils import join_col_vals

df_prices = pd.read_csv('data/mat_prices.csv', index_col=0)
df_physprop = pd.read_csv('data/physprops.csv', index_col=0)


# %%
# [df_prices[p] for p in df_physprop.index
# df_physprop.index

with open('output/missing_data.txt', 'w') as f:
    f.write("---Property data without a price---\n\n")
    for idx, row in df_physprop.iterrows():
        if idx not in df_prices.index:
            f.write("{}, {}  ({})".format(idx, row['original_name'], row['source']))
            f.write("\n")

    f.write("\n---Unused Price data---\n\n")
    for idx, row in df_prices.iterrows():
        if idx not in df_physprop.index:
            f.write("{} ({})".format(idx, row['source']))
            f.write("\n")
    # f.write("\n\n---Price data without property--\n")
    # f.write("\n".join([f for f in df_prices.index if f not in df_physprop.index]))
    # %%
