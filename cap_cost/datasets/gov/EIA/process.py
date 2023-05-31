#%%

import pandas as pd
# import pint_pandas
from es_utils.units import ureg
from es_utils.cpi import get_cpi_data

s = pd.read_csv('input_data/United_States_Natural_Gas_Industrial_Price.csv', skiprows=4, index_col=0, parse_dates=True, squeeze=True)


s = s.astype('pint[USD/cubic_foot]')
s = s/1000
# s = s.pint.to('USD/kWh')

# s.pint.magnitude.plot()

s = s.sort_index()
s = s.last('10Y')

#%%

# cpi_data = get_cpi_data(2022)

s_year = s.resample('Y').mean()
s_year.index = s_year.index.year
# s_year = s_year*cpi_data[s_year.index]

SP_vol = s_year.mean()

SP_vol

#%%

from es_utils.chem import get_molecular_mass

R = ureg.Quantity(8.3145, 'J/mol/K')
T = ureg.Quantity(330, 'K')
P = ureg.Quantity(1,'atm')
mu_CH4 = ureg.Quantity(get_molecular_mass('CH4'), 'g/mol')


mass_densities_gas = (mu_CH4*P)/(R*T)

mass_densities_gas = mass_densities_gas.to('kg/m**3')
mass_densities_gas
# mass_densities_gas = mass_densities_gas.dropna()


#%%

SP = SP_vol/mass_densities_gas

SP = SP.to('USD/kg')


SP

#%%

from es_utils.units import prep_df_pint_out

mat_dict = {
    'molecular_formula': ['CH4'],
    'source': ['EIA Henry Hub'],
    'notes': ["Average over last 10 Years"],
    'specific_price': [SP.magnitude]
}

df_mat = pd.DataFrame(mat_dict,index = ['Fossil CH4'])
df_mat.index.name = 'index'

df_mat['specific_price'] = df_mat['specific_price'].astype('pint[USD/kg]')

df_mat = prep_df_pint_out(df_mat)

df_mat.to_csv('output/mat_data.csv')
