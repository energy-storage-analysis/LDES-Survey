"""
Processing script template. This template is designed to work on extracted data (e.g. tables from pdf obtained from extract_template.py)
"""

#%%
import pandas as pd
import os
from es_utils.units import prep_df_pint_out, convert_units
from es_utils.chem import process_mat_lookup
from es_utils.units import ureg
from es_utils.chem import get_molecular_mass

if not os.path.exists('output'): os.mkdir('output')
tables = {fn.strip('.csv') : pd.read_csv(os.path.join('tables',fn), encoding='utf-8', index_col=0) for fn in os.listdir('tables')}
#%%

# Output the columns of a table into the Ipython console and copy to the rename dictonary below to rename the columns. 

df = tables['table_1']

df = df.reset_index()

df = df.rename({
'Volume (m3) ': 'tank_vol',
'Max. pressure (MPa)':'P_max', 
'Min. pressure (MPa)': 'P_min',
'Volume capacity (m3\n(STP))': 'vol_cap', 
'Volume capacity (m3\r\n(STP))': 'vol_cap', #TODO: new line character seems to keep switching...
'Investment (€) ': 'total_cost',
'Spec. investment (€ m − 3\n(STP))':'vol_cost',
'Spec. investment (€ m − 3\r\n(STP))':'vol_cost'
}, axis=1)

# df.index.name = 'original_name'
# df = df.drop([], axis=1)
# df = df[['vol_cost']]

df

#%%

#The volumne cost is calculated based on STP, so no need to take into account pressures. 
vol_cost = ureg.Quantity(df['vol_cost'].mean(),'EUR/m**3')


mu_H2 = get_molecular_mass('H2')
mu_H2 = ureg.Quantity(mu_H2, 'g/mol')

P_cavern = ureg.Quantity(1, 'atm')
T = ureg.Quantity(273.15, 'K')
R = ureg.Quantity(8.3145, 'J/mol/K')

mass_density_H2_STP = (mu_H2*P_cavern)/(R*T)
mass_density_H2_STP = mass_density_H2_STP.to('kg/m**3')
mass_density_H2_STP

#%%



vol_cost = vol_cost.to('USD/m**3')

mass_cost = vol_cost/mass_density_H2_STP
mass_cost = mass_cost.to('USD/kg').magnitude

mass_cost

mat_dict = {
    'specific_price': [mass_cost],
    'molecular_formula': ['H2']
}

df_mat = pd.DataFrame(mat_dict, index = ['H2 Spherical Pressure'])
df_mat['specific_price'] = df_mat['specific_price'].astype('pint[USD/kg]')
df_mat.index.name = 'index'

df_mat
df_mat = convert_units(df_mat)
df_mat = prep_df_pint_out(df_mat)

df_mat.to_csv('output/mat_data.csv')

#%%

deltaG_H2 = 0.0659 #kWh/molH2

SM_dict = {
    'deltaG_chem': [deltaG_H2],
    'n_e': [2],
    'materials': ["H2 Spherical Pressure"],
    'SM_type': ['synfuel'],
    'sub_type': ['tank'],
    'mat_basis': ['molar'],
}

df_SM = pd.DataFrame(SM_dict,index = ['H2 Spherical Pressure'])

df_SM = df_SM.astype({
    'deltaG_chem': 'pint[kWh/mol]',
    'n_e': 'pint[dimensionless]'
})

df_SM = convert_units(df_SM)
df_SM = prep_df_pint_out(df_SM)
df_SM.to_csv('output/SM_data.csv')
# Create these files, delete columns other than original_name, then add lookup columns as describd in readme


# df.to_csv('SM_lookup.csv')
# df.to_csv('mat_lookup.csv')
#%%