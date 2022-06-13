#%%
import pandas as pd
import os
if not os.path.exists('output'): os.makedirs('output')

from es_utils.units import convert_units, prep_df_pint_out, ureg
from es_utils import join_col_vals
from es_utils.cpi_util import cpi_data

#%%
# Convert hydrogen chemical to volumetric

df_H2 = pd.read_csv('H2_specific.csv')

R = ureg.Quantity(8.3145, 'J/mol/K')
T = ureg.Quantity(330, 'K')
mu_H2 = ureg.Quantity(2, 'g/mol')

P = df_H2['pressure'].astype('pint[Pa]')

mass_density = mu_H2*P/(R*T)
mass_density


def convert_row(df, val_col, unit_col, unit_to):
    """Converts the val_col of a dataframe to units of unit_to based on unit_col starting units"""
    data_out = []
    for index, row in df.iterrows():
        unit = row[unit_col]
        val = row[val_col]
        val = ureg.Quantity(val, unit)
        val = val.to(unit_to).magnitude
        data_out.append(val)

    data_out = pd.Series(data_out, index=df.index, dtype="pint[{}]".format(unit_to)) 

    return data_out

specific_price = convert_row(df_H2, 'H2_specific_cost', 'unit', 'USD/kg')

df_H2['vol_cost'] = specific_price*mass_density
df_H2['vol_cost'] = df_H2['vol_cost'].pint.to('USD/m**3')

#%%
#Add in costs already specified in volumetric terms 

df_vol = pd.read_csv('vol_data.csv')

df_vol['vol_cost'] = convert_row(df_vol, 'vol_cost', 'unit', 'USD/m**3')

df_vol_all = pd.concat([
    df_H2[['type','vol_cost','year','source']],
    df_vol[['type','vol_cost','year','source']]
])


df_vol_all['vol_cost'] = df_vol_all['vol_cost']*cpi_data[df_vol_all['year']].values

df_vol_all.to_csv('output/vol_cost_all.csv')


#%%
#Average volumetric costs between sources

vol_costs = df_vol_all.groupby('type')['vol_cost'].mean()
vol_costs.name = 'vol_cost'

sources = df_vol_all.groupby('type')['source'].apply(join_col_vals)
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