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


from es_utils.units import ureg

# Previously calculated value for solar salt

# %%

df_SMs = read_pint_df(pjoin(REPO_DIR,'cap_cost/data_consolidated/SM_data.csv'), index_col=[0,1]).reset_index('SM_type')
# %%

Cp = df_SMs['Cp'].dropna().pint.to('kWh/(kg*K)')

Cp.pint.magnitude.plot.hist()

#%%

# from pint import Quantity

Cp500 = Cp*ureg.Quantity(500, 'K') 

Cp500

#%%

Cp500.pint.magnitude.plot.hist()


DP = ureg.Quantity(1.5, 'kJ/kg/K')
DP500 = DP*ureg.Quantity(500,'K')

print("Dulong Petit Law at 500 K for solar salt: {}".format(DP500.to('kWh/kg')))

#%%

solar_salt_price = ureg.Quantity(0.6, 'USD/kg')

CkWh = solar_salt_price/DP500

CkWh.to('USD/kWh')