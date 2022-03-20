#%%
from cgitb import lookup
import os
from os.path import join as pjoin
import numpy as np
import pandas as pd
from es_utils import join_col_vals

df_prices = pd.read_csv('data/mat_prices.csv', index_col=0)
df_physprop = pd.read_csv('data/mat_physprop.csv', index_col=0)
df_SMs = pd.read_csv('data/SMs.csv', index_col=0)

#%%


# sensible_thermal = (df_physprop['Cp']*500)
# sensible_thermal.name='specific_energy'
# sensible_thermal = sensible_thermal.to_frame()
# sensible_thermal['energy_type'] = 'Thermal (Sensible)'

# latent_thermal = (df_physprop['sp_latent_heat'])
# latent_thermal.name='specific_energy'
# latent_thermal = latent_thermal.to_frame()
# latent_thermal['energy_type'] = 'Thermal (Latent)'

# thermochem = (df_physprop['deltaH_thermochem'])
# thermochem.name='specific_energy'
# thermochem = thermochem.to_frame()
# thermochem['energy_type'] = 'Chemical (Thermochemical)'

# chemical = (df_physprop['deltaG_chem'])
# chemical.name='specific_energy'
# chemical = chemical.to_frame()
# chemical['energy_type'] = 'Chemical (Syn. Fuel)'

# virial = (df_physprop['specific_strength']/3600) #TODO:Assuming Q=1
# virial.name='specific_energy'
# virial = virial.to_frame()
# virial['energy_type'] = 'Viral Limited'


# epsilon_0 = 8.85e-12
# def calc_electrostatic_SE(V_breakdown, dielectric_const, rho_m):
#     specific_energy = 0.5*(V_breakdown**2)*dielectric_const*epsilon_0 #J/m3
#     specific_energy = specific_energy/(rho_m*1000) #J/kg
#     specific_energy = specific_energy/3600000 #kWh/kg
#     return specific_energy

# electrostatic = calc_electrostatic_SE(
#     V_breakdown=df_physprop['dielectric_breakdown'],
#     dielectric_const=df_physprop['dielectric_constant'],
#     rho_m = df_physprop['mass_density']
# )
# electrostatic.name='specific_energy'
# electrostatic = electrostatic.to_frame()
# electrostatic['energy_type'] = 'Electrostatic (Capacitor)'


# #TODO: need to implement pseudocapactior. As well as make deltaV work with batteries
# electrostatic_edlc = (0.5*df_physprop['specific_capacitance']*df_physprop['deltaV']**2) #J/g
# electrostatic_edlc = electrostatic_edlc/3600

# electrostatic_edlc.name='specific_energy'
# electrostatic_edlc = electrostatic_edlc.to_frame()
# electrostatic_edlc['energy_type'] = 'Electrostatic (EDLC)'



# gravitational = (df_physprop['delta_height']*9.81/3600000)
# gravitational.name='specific_energy'
# gravitational = gravitational.to_frame()
# gravitational['energy_type'] = 'Gravitational'

# dfs = [
#     chemical,
#     thermochem,
#     sensible_thermal,
#     latent_thermal,
#     virial,
#     electrostatic_edlc,
#     electrostatic,
#     gravitational
# ]

# dfs_2 = []
# for df in dfs:
#     df['physprop_source'] = df_physprop['source']
#     df['original_name'] = df_physprop['original_name']
#     dfs_2.append(df)

# df_out = pd.concat(dfs_2).dropna()


# df_out

# #%%
# prices = [df_prices['specific_price'][p] if p in df_prices.index else np.nan for p in df_out.index]
# sources = [df_prices['source'][p] if p in df_prices.index else np.nan for p in df_out.index]

# df_out['specific_price'] = prices
# df_out['price_sources'] = sources


# # #drop any whwere price or energy data is missing
# # #TODO: make aware of missing prices and materials 
# # df_out = df_out.dropna(subset=['specific_price', 'specific_energy'], how='any')

# df_out

#%%


df_SMs.index.name = 'index'
df_SMs['original_name'] = df_SMs.index #TODO:
df_SMs




def get_mat_info_list(l, column, lookup_df):
    l = l.strip('][').split(', ')
    l_mu = []
    for f in l:
        f = str(f)
        f= f.strip('\'')
        if f not in lookup_df.index:
            print(f)
            return np.nan
        l_mu.append(lookup_df[column].loc[f])
    return l_mu

df_SMs['mus'] = df_SMs['materials'].apply(get_mat_info_list, column='mu', lookup_df=df_physprop)
df_SMs['mu_total'] = df_SMs['mus'].apply(np.sum)
df_SMs['prices'] = df_SMs['materials'].apply(get_mat_info_list, column='specific_price', lookup_df=df_prices)
df_SMs['price_sources'] = df_SMs['materials'].apply(get_mat_info_list, column='source', lookup_df=df_prices)
df_SMs

#%%
df_SMs.where(df_SMs['mus'].isna()).dropna(how='all')['materials']

#TODO: all energy types are electrochemical temporarily
F = 96485 # C/mol
df_SMs['specific_energy'] = (1/3600)*F*df_SMs['deltaV']/df_SMs['mu_total']
#%%

df_SMs = df_SMs.dropna(subset=['mus'])

specific_price_totals = []

for idx, row in df_SMs.iterrows():
    # mats = row['materials']
    mus = row['mus']
    mu_total = row['mu_total'] #Should be the same as sum(mus), but needed for specific energy...
    SPs = row['prices']

    #Arrays should be the same length
    #TODO: chech this equation
    weighted_SPs = []
    for i in range(len(mus)):
        weighted_SP = (mus[i]*SPs[i])/mu_total
        weighted_SPs.append(weighted_SP)
    
    specific_price_total = sum(weighted_SPs)
    specific_price_totals.append(specific_price_total)



df_SMs['specific_price'] = specific_price_totals

df_SMs = df_SMs.rename({'source': 'physprop_source'}, axis=1)

df_SMs

#%%
import ast

df_sensible_thermal = df_SMs.where(df_SMs['energy_type'] == 'sensible_thermal').dropna(how='all')

single_mat = df_sensible_thermal['materials'].str.strip('][')

Cp = df_physprop.loc[single_mat]['Cp']

df_SMs['specific_energy'].loc[df_sensible_thermal.index] = Cp*500



# df_latent_thermal['mat']

#%%
df_out = df_SMs

# df_out = pd.concat([
#     df_SMs[['specific_energy', 'energy_type','specific_price','physprop_source', 'price_sources', 'original_name']],
#     df_out,
# ])

df_out['C_kwh'] = df_out['specific_price']/df_out['specific_energy']

# df_out = df_out.dropna(subset=['C_kwh'])

# %%

df_out.to_csv('data/C_kwh.csv')

# %%
