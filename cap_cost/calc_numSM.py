"""
This script calculates the number of storage media that use a given price. This
was originally included in consolidate_data.py, but this needs to be done after
calculating CkWh so that storage media without CkWh (due to not having a
combination of physical property or price?) can not be included in this
statistic

TODO: combine all gen dataset scripts togehter? 
TODO: List out missing physical properties like prices. 
"""


#%%

import os
from os.path import join as pjoin
import numpy as np
import pandas as pd
from es_utils import join_col_vals
from es_utils.units import prep_df_pint_out, read_pint_df, ureg


df_mat_data = read_pint_df('data_consolidated/mat_data.csv')

df_SMs =  read_pint_df('data_consolidated/SM_data.csv', index_col=[0,1])


import ast
mats = df_SMs['materials']

mats_single = mats.where(~mats.str.contains('[', regex=False)).dropna()
mats_comp = mats.where(mats.str.contains('[', regex=False)).dropna()
mats_comp = mats_comp.apply(ast.literal_eval)



num_sms = []
for idx in df_mat_data.index:
    n = 0 
    for mat_name in mats_single.values:
        if mat_name == idx:
            n = n+1
    for comp_list in mats_comp:
        mats = [t[0] for t in comp_list]
        if idx in mats:
            n = n+1

    num_sms.append(n)

df_mat_data['num_SMs'] = num_sms


df_mat_data = df_mat_data[[
'specific_price', 'specific_price_std','specific_price_rat', 'vol_price','num_SMs', 'num_source','sources','specific_prices','molecular_formula','mu','original_names','specific_price_element',
]]

# %%


df_mat_data = prep_df_pint_out(df_mat_data)

df_mat_data.to_csv('data_consolidated/mat_data.csv')