#%%
import pandas as pd
import os
if not os.path.exists('output'): os.makedirs('output')

df_H2 = pd.read_csv('H2_specific.csv')

R=8.3145
T=330

df_H2['mass_density'] = (2/1000)*df_H2['pressure']/(R*T)

df_H2['vol_cost'] = df_H2['H2_specific_cost']*df_H2['mass_density']

df_H2

#%%

df_vol = pd.read_csv('vol_data.csv')

df_vol

#%%

df_vol_all = pd.concat([
    df_H2[['type','vol_cost','source']],
    df_vol[['type','vol_cost','source']]
])

vol_costs = df_vol_all.groupby('type')['vol_cost'].mean()
vol_costs.name = 'vol_cost'

from es_utils import join_col_vals

sources = df_vol_all.groupby('type')['source'].apply(join_col_vals)
sources.name='sources'

df_vol_final = pd.concat([
vol_costs,
sources,
],axis=1)

df_vol_final

df_vol_final.to_csv('output/vol_cost.csv')

#%%

df_gas = pd.read_csv('gasses.csv', index_col=0)
df_gas['mu'] = df_gas['mu']/1000 #kg/mol

P_cavern = 1e7
T=330

df_gas['mass_density'] = (df_gas['mu']*P_cavern)/(R*T)

df_gas.loc['H2O', 'mass_density'] = 1000

sm_names = []
SPs = []
mol_forms = []
mass_densities = []
for sm_type, row in df_vol_final.iterrows():
    vol_cost = row['vol_cost']
    for gas in df_gas.index:
        rho_m = df_gas['mass_density'][gas]
        specific_price = vol_cost/rho_m

        sm_names.append("{}_{}".format(gas,sm_type))
        SPs.append(specific_price)
        mol_forms.append(gas)
        mass_densities.append(df_gas['mass_density'][gas])

df_mat = pd.Series(SPs, index=sm_names)
df_mat.name = 'specific_price'
df_mat = df_mat.to_frame()

df_mat['molecular_formula'] = mol_forms
df_mat['mass_density'] = mass_densities

df_mat.index.name = 'index'

df_mat.to_csv('output/mat_data.csv')