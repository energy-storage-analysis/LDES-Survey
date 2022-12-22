#%%
import pandas as pd
import os

from es_utils.units import ureg, prep_df_pint_out

if not os.path.exists('output'): os.mkdir('output')
tables = {fn.strip('.csv') : pd.read_csv(os.path.join('tables',fn), encoding='utf-8', index_col=0) for fn in os.listdir('tables')}
#%%

df_2 = tables['table_2'].T

for col in df_2.columns:
    df_2[col] = df_2[col].str.replace('$','', regex=False)
    df_2[col] = df_2[col].str.replace(',','', regex=False)
    df_2[col] = df_2[col].astype(float)

df_2['cavern_cost'] = df_2['Dome ($/kg)'] #+ df_2['Liner ($/kg)'] + df_2['Concrete ($/kg)']

df_2

#%%
df_3 = tables['table_3'].T

for col in df_3.columns:
    df_3[col] = df_3[col].str.replace('$','', regex=False)
    df_3[col] = df_3[col].str.replace(',','', regex=False)
    df_3[col] = df_3[col].astype(float)

df_3

df_3.to_csv('output/table_3_processed.csv')

#%%

#Don't include Teeside, as it is not a pressurized cavern
#%%



df_out = pd.DataFrame(columns=['cost_H2', 'P'])
df_out.index.name = 'index'

leaching_cost = float(df_3.loc['2000']['Leaching ($/kg)'])

#This is the fraction of leaching costs calculated from lord 2014 data (see Readme)
leaching_cost = leaching_cost *  0.5715509854327335

df_out.loc['Salt Cavern', 'cost_H2'] = leaching_cost
df_out.loc['Salt Cavern', 'P'] = 100

df_out.loc['LRC', 'cost_H2'] = df_2.loc['100']['cavern_cost']
df_out.loc['LRC', 'P'] = 100

df_out['cost_H2'] =df_out['cost_H2'].astype('pint[USD/kg]')
df_out['P'] =df_out['P'].astype('pint[atm]')

df_out

#%%



R = ureg.Quantity(8.3145, 'J/mol/K')
T = ureg.Quantity(330, 'K')
mu_H2 = ureg.Quantity(2, 'g/mol')

P = df_out['P'].astype('pint[Pa]')

mass_density = mu_H2*P/(R*T)
mass_density


df_out['vol_price'] = df_out['cost_H2']*mass_density
df_out['vol_price'] = df_out['vol_price'].pint.to('USD/m**3')


df_out = df_out[['vol_price']]

df_out


#%%

df_out = prep_df_pint_out(df_out)

df_out.to_csv('output/mat_data.csv')


# df.to_csv('SM_lookup.csv')
#%%

# df = df.rename({}, axis=1)

# SM_lookup = pd.read_csv('SM_lookup.csv')
# df = pd.merge(df_t3, SM_lookup, on='original_name')
# df = df.dropna(subset=['SM_name'])
# df = df.set_index('SM_name')


# %%

# df.to_csv('output/SM_data.csv')