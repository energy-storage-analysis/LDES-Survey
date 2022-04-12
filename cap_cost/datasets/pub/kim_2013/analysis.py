#%%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df_couples = pd.read_csv('output/couples.csv', index_col=0)
df_couples=  df_couples.dropna(subset=['deltaV'])

df_prices = pd.read_csv('output/prices.csv', index_col=0)

#%%

df_couples['SP_A'] = df_prices.loc[df_couples['A']]['specific_price'].values
df_couples['SP_B'] = df_prices.loc[df_couples['B']]['specific_price'].values


#TODO: chech this equation
df_couples['specific_price'] = (df_couples['SP_A']*df_couples['mu_A'] + df_couples['SP_B']*df_couples['mu_B'])/(df_couples['mu_A']+df_couples['mu_B'])



df_couples['C_kwh'] = df_couples['specific_price']/df_couples['specific_energy']

df_couples.sort_values('C_kwh')

#%%

bins = np.logspace(np.log10(1), np.log10(1e6), 50)
df_couples['C_kwh'].hist(bins=bins)

plt.xscale('log')
# %%
