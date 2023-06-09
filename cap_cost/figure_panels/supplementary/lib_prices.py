

#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
from es_utils.units import read_pint_df
# plt.rcParams.update({'font.size':16, 'savefig.dpi': 600})

plt.rcParams.update({
    "savefig.facecolor": 'white',
    "font.size": 7, 
    'savefig.dpi': 600, 
    'font.sans-serif': 'arial', 
    'figure.figsize': (2.3, 1.6)
})

grid = False


import os
from os.path import join as pjoin


from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

# %%

df_SMs = read_pint_df(pjoin(REPO_DIR,'cap_cost/data_consolidated/SM_data.csv'), index_col=[0,1], drop_units=True).reset_index('SM_type')
# %%

df_sel = df_SMs.where(
    df_SMs['SM_type'] == 'coupled_battery').dropna(how='all')


df_sel = df_sel.where(df_sel['mat_type'] == 'Li ion').dropna(how='all')


df_rem = df_sel.where(df_sel['C_kwh'] > 200).dropna(how='all').dropna(how='all',axis=1)
print("removing batteries above Diurnal regime")
print(df_rem)

#Remove 2 outlier chemistries
df_sel = df_sel.where(df_sel['C_kwh'] < 200).dropna(how='all')


df_sel['C_kwh'].plot.hist()

plt.xlabel(" $C_{kWh,SM} [USD/kWh]$")
plt.ylabel("Count")

plt.suptitle("Average Price: {:0.1f} USD/kWh".format(df_sel['C_kwh'].mean()))


# print("mean: {}".format(df_sel['C_kwh'].mean()))
# print("median: {}".format(df_sel['C_kwh'].median()))

plt.tight_layout()

plt.savefig('figures/LIB_Prices.png')
# %%
