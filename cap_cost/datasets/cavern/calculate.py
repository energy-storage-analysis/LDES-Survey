#%%
import pandas as pd
import os
if not os.path.exists('output'): os.makedirs('output')

from es_utils.units import convert_units, prep_df_pint_out, ureg, read_pint_df
from es_utils import join_col_vals

#%%

df_pap = read_pint_df('papadias_2021/output/vol_cost.csv')
df_pap['source'] = 'Papadias 2021'
df_eti = read_pint_df('ETI_2018/output/vol_cost.csv')
df_eti['source'] = 'ETI 2018'

df_vol = pd.concat([
    df_pap,
    df_eti
])

df_vol.to_csv('output/vol_cost_all.csv')


#%%
#Average volumetric costs between sources


R = ureg.Quantity(8.3145, 'J/mol/K')

vol_costs = df_vol.groupby('index')['vol_cost'].mean()
vol_costs.name = 'vol_cost'

sources = df_vol.groupby('index')['source'].apply(join_col_vals)
sources.name='sources'

df_vol_final = pd.concat([
vol_costs,
sources,
],axis=1)

df_vol_final.to_csv('output/vol_cost.csv')

#%%
#Calculate the specific costs for different gasses

df_gas = pd.read_csv('gasses.csv', index_col=0)
df_gas['mu'] = df_gas['mu'].astype('pint[g/mol]')

P_cavern = ureg.Quantity(1e7, 'Pa')
T = ureg.Quantity(330, 'K')

df_gas['mass_density'] = (df_gas['mu']*P_cavern)/(R*T)
df_gas['mass_density'] = df_gas['mass_density'].pint.to('kg/m**3')

print(df_gas['mass_density'])


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


df_mat = df_mat.astype({
    'specific_price': 'pint[USD/kg]',
    'mass_density': 'pint[kg/m**3]'
})


df_mat = prep_df_pint_out(df_mat)

df_mat.to_csv('output/mat_data.csv')
# %%
