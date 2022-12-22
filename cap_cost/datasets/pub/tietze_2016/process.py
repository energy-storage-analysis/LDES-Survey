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


#The volumne cost is calculated based on STP, so no need to take into account pressures. 
vol_cost = ureg.Quantity(df['vol_cost'].mean(),'EUR/m**3')
vol_cost = vol_cost.to('USD/m**3')


#%%
mat_dict = {
    'vol_price': [vol_cost],
}

df_mat = pd.DataFrame(mat_dict, index = ['Spherical Pressure'])
df_mat['vol_price'] = df_mat['vol_price'].astype('pint[USD/m**3]')
df_mat.index.name = 'index'

df_mat
df_mat = convert_units(df_mat)
df_mat = prep_df_pint_out(df_mat)

df_mat.to_csv('output/mat_data.csv')


#%%



#%%

P_tank = ureg.Quantity(1, 'atm')
T = ureg.Quantity(273.15, 'K')
R = ureg.Quantity(8.3145, 'J/mol/K')

mu_H2 = get_molecular_mass('H2')
mu_H2 = ureg.Quantity(mu_H2, 'g/mol')
mass_density_H2_STP = (mu_H2*P_tank)/(R*T)
mass_density_H2_STP = mass_density_H2_STP.to('kg/m**3')
# mass_cost_H2 = vol_cost/mass_density_H2_STP
# mass_cost_H2 = mass_cost_H2.to('USD/kg').magnitude

mu_CH4 = get_molecular_mass('CH4')
mu_CH4 = ureg.Quantity(mu_CH4, 'g/mol')
mass_density_CH4_STP = (mu_CH4*P_tank)/(R*T)
mass_density_CH4_STP = mass_density_CH4_STP.to('kg/m**3')
# mass_cost_CH4 = vol_cost/mass_density_CH4_STP
# mass_cost_CH4 = mass_cost_CH4.to('USD/kg').magnitude
#TODO: handle with lookup table...Can we use a consistent deltaG for all snythetic fuel calculations (including feedstock for example) vs copying it into the code like this

deltaG_H2 = 0.0659 #kWh/molH2
deltaG_CH4 =  0.2554 #kWh/molCH4 #TODO: Check

SM_dict = {
    'SM_type': ['synfuel', 'synfuel'],
    'sub_type': ['tank', 'tank'],
    'materials': ["Spherical Pressure", "Spherical Pressure"],
    'mat_basis': ['', ''],
    'deltaG_chem': [deltaG_H2, deltaG_CH4],
    'n_e': [2, 8],
    'mass_density': [mass_density_H2_STP, mass_density_CH4_STP],
    'mu_total': [mu_H2, mu_CH4]
}

df_SM = pd.DataFrame(SM_dict,index = ['H2 Spherical Pressure', 'CH4 Spherical Pressure'])

df_SM = df_SM.astype({
    'deltaG_chem': 'pint[kWh/mol]',
    'n_e': 'pint[dimensionless]',
    'mass_density': 'pint[kg/m**3]',
    'mu_total': 'pint[g/mol]'
})

df_SM = convert_units(df_SM)
df_SM = prep_df_pint_out(df_SM)
df_SM.to_csv('output/SM_data.csv')
# Create these files, delete columns other than original_name, then add lookup columns as describd in readme


# df.to_csv('SM_lookup.csv')
# df.to_csv('mat_lookup.csv')
#%%