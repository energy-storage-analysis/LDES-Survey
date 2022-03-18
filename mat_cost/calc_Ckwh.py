#%%
import os
from os.path import join as pjoin
import numpy as np
import pandas as pd
from es_utils import join_col_vals

df_prices = pd.read_csv('data/mat_prices.csv', index_col=0)
df_physprop = pd.read_csv('data/physprops.csv', index_col=0)

#%%


sensible_thermal = (df_physprop['Cp']*500)
sensible_thermal.name='specific_energy'
sensible_thermal = sensible_thermal.to_frame()
sensible_thermal['energy_type'] = 'Thermal (Sensible)'

latent_thermal = (df_physprop['sp_latent_heat'])
latent_thermal.name='specific_energy'
latent_thermal = latent_thermal.to_frame()
latent_thermal['energy_type'] = 'Thermal (Latent)'

thermochem = (df_physprop['deltaH_thermochem'])
thermochem.name='specific_energy'
thermochem = thermochem.to_frame()
thermochem['energy_type'] = 'Chemical (Thermochemical)'

chemical = (df_physprop['deltaG_chem'])
chemical.name='specific_energy'
chemical = chemical.to_frame()
chemical['energy_type'] = 'Chemical (Syn. Fuel)'

virial = (df_physprop['specific_strength']/3600) #TODO:Assuming Q=1
virial.name='specific_energy'
virial = virial.to_frame()
virial['energy_type'] = 'Viral Limited'


epsilon_0 = 8.85e-12
def calc_electrostatic_SE(V_breakdown, dielectric_const, rho_m):
    specific_energy = 0.5*(V_breakdown**2)*dielectric_const*epsilon_0/rho_m #J/m3
    specific_energy = specific_energy/(rho_m*1000) #J/kg
    specific_energy = specific_energy/3600000 #kWh/kg
    return specific_energy

electrostatic = calc_electrostatic_SE(
    V_breakdown=df_physprop['dielectric_breakdown'],
    dielectric_const=df_physprop['dielectric_constant'],
    rho_m = df_physprop['mass_density']
)
electrostatic.name='specific_energy'
electrostatic = electrostatic.to_frame()
electrostatic['energy_type'] = 'Electrostatic (Capacitor)'

gravitational = (df_physprop['delta_height']*9.81/3600000)
gravitational.name='specific_energy'
gravitational = gravitational.to_frame()
gravitational['energy_type'] = 'Gravitational'

dfs = [
    chemical,
    thermochem,
    sensible_thermal,
    latent_thermal,
    virial,
    electrostatic,
    gravitational
]

dfs_2 = []
for df in dfs:
    df['physprop_source'] = df_physprop['source']
    df['original_name'] = df_physprop['original_name']
    dfs_2.append(df)

df_out = pd.concat(dfs_2).dropna()


df_out

#%%
prices = [df_prices['specific_price'][p] if p in df_prices.index else np.nan for p in df_out.index]
sources = [df_prices['source'][p] if p in df_prices.index else np.nan for p in df_out.index]

df_out['specific_price'] = prices
df_out['price_sources'] = sources


# #drop any whwere price or energy data is missing
# #TODO: make aware of missing prices and materials 
# df_out = df_out.dropna(subset=['specific_price', 'specific_energy'], how='any')

df_out

#%%
df_ec_li = pd.read_csv(r'C:\Users\aspit\Git\MHDLab-Projects\Energy-Storage-Analysis\datasets\pub\li_2017\output\couples.csv',index_col=0)
df_ec_li['physprop_source'] = 'Li 2017'
df_ec_lmb = pd.read_csv(r'C:\Users\aspit\Git\MHDLab-Projects\Energy-Storage-Analysis\datasets\pub\kim_2013\output\couples.csv', index_col=0)
df_ec_lmb['type'] = 'Liquid Metal'
df_ec_lmb['physprop_source'] = 'Kim 2013'

col_select = ['type','A','B','mu_A', 'mu_B', 'deltaV', 'specific_energy', 'physprop_source']

df_ec = pd.concat([
    df_ec_li[col_select],
    df_ec_lmb[col_select],
])

df_ec['SP_A'] = [df_prices['specific_price'][f] if f in df_prices.index else np.nan for f in df_ec['A']]
df_ec['price_source_A'] = [df_prices['source'][f] if f in df_prices.index else np.nan for f in df_ec['A']]
df_ec['SP_B'] = [df_prices['specific_price'][f] if f in df_prices.index else np.nan for f in df_ec['B']]
df_ec['price_source_B'] = [df_prices['source'][f] if f in df_prices.index else np.nan for f in df_ec['B']]

df_ec['price_sources'] = "A: " + df_ec['price_source_A'] + " --- B: " + df_ec['price_source_B']

#TODO: chech this equation
df_ec['specific_price'] = (df_ec['SP_A']*df_ec['mu_A'] + df_ec['SP_B']*df_ec['mu_B'])/(df_ec['mu_A']+df_ec['mu_B'])

df_ec['energy_type'] = 'Chemical (EC Couple)'
df_ec.index.name = 'index'
df_ec['original_name'] = df_ec.index
df_ec['price_type'] = 'TODO'

df_ec.to_csv('data/df_couples.csv')

#%%


df_out = pd.concat([
    df_ec[['specific_energy', 'energy_type','specific_price','physprop_source', 'price_sources', 'original_name']],
    df_out,
])

df_out['C_kwh'] = df_out['specific_price']/df_out['specific_energy']

df_out = df_out.dropna(subset=['C_kwh'])

# %%

df_out.to_csv('data/C_kwh.csv')

# %%
