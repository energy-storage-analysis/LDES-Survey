
"""
This script generates tables with information/stats about the final dataset
"""
#%%
import pandas as pd
import matplotlib.pyplot as plt
from es_utils.units import read_pint_df

import os
from os.path import join as pjoin

from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

df_mat_data = read_pint_df(pjoin(REPO_DIR, 'cap_cost/data_consolidated/mat_data_all.csv'), index_col=0, drop_units=True)
# %%


df = pd.to_datetime(df_mat_data['year'], format="%Y").dt.year

df.value_counts().sort_index().plot(kind='bar')

plt.ylabel("Count")
plt.xlabel("Source Year")

plt.savefig('figures/inflation_year_counts.png')

# %%
