#%%
import pandas as pd
import os
if not os.path.exists('output'): os.makedirs('output')

from es_utils.units import convert_units, prep_df_pint_out, ureg, read_pint_df
from es_utils import join_col_vals

#%%
#Calculate the specific costs for different gasses

df = read_pint_df('SM_def.csv')

from es_utils.chem import get_molecular_mass


df['mu_total'] = df['molecular_formula'].apply(get_molecular_mass)
df['mu_total'] = df['mu_total'].astype('pint[g/mol]')
df

#%%


R = ureg.Quantity(8.3145, 'J/mol/K')
# df_gas = pd.read_csv('gasses.csv', index_col=0)
# df_gas['mu'] = df_gas['mu'].astype('pint[g/mol]')

# P_cavern = ureg.Quantity(1e7, 'Pa')
T = ureg.Quantity(293.15, 'K')

mass_densities_gas = (df['mu_total']*df['P_cavern'])/(R*T)
mass_densities_gas = mass_densities_gas.pint.to('kg/m**3')
# mass_densities_gas = mass_densities_gas.dropna()

df['mass_density'] = mass_densities_gas

# %%

#TODO: this is a quick fix to remove pressures from synfuel storage media, other wise calc_Ckwh tries to calculate pressure energy and ends up with a duplicated index. Need to allow for multiple energy types.
import numpy as np
synfuel_idx = df[df['SM_type'] == 'synfuel'].index
df['P_cavern'].loc[synfuel_idx] = np.nan
#%%


df_out = prep_df_pint_out(df)

df_out = df_out.drop('molecular_formula', axis=1)

df_out.to_csv('output/SM_data.csv')