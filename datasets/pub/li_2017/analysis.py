#%%

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#%%
df_prices = pd.read_csv('output/prices.csv')
df_prices = df_prices.dropna(subset = ['molecular_formula']).set_index('molecular_formula')
s_prices = df_prices['specific_price']

#%%
df_couples = pd.read_csv('output/couples.csv',index_col=0)
df_couples['SP_A'] = [s_prices[f] if f in s_prices.index else np.nan for f in df_couples['A']]
df_couples['SP_B'] = [s_prices[f] if f in s_prices.index else np.nan for f in df_couples['B']]
df_couples
#%%

#TODO: chech this equation
#TODO: should we be including the O2 for the air price, artificially lowers as we are not actually buying those kg. 
df_couples['specific_price'] = (df_couples['SP_A']*df_couples['mu_A'] + df_couples['SP_B']*df_couples['mu_B'])/(df_couples['mu_A']+df_couples['mu_B'])


df_couples['C_kwh'] = df_couples['specific_price']/df_couples['specific_energy']
# %%

# %%
df_couples.sort_values('C_kwh')

#%%

bins = np.logspace(np.log10(1), np.log10(1e3), 50)
df_couples['C_kwh'].hist(bins=bins)

plt.xscale('log')
plt.xlabel('$/kWh')
plt.ylabel('Count')

# %%


plt.scatter(df_couples['C_kwh_orig'], df_couples['C_kwh'])
plt.yscale('log')
plt.xscale('log')


#%%

orig_calc_ratio = df_couples['C_kwh_orig']/df_couples['C_kwh']
orig_calc_ratio = orig_calc_ratio.dropna()
orig_calc_ratio
# %%
orig_calc_ratio.sort_values()[0:10]
#%%
orig_calc_ratio.sort_values(ascending=False)[0:10]