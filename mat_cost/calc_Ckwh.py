#%%
from cgitb import lookup
import os
from os.path import join as pjoin
import numpy as np
import pandas as pd
from es_utils import join_col_vals

df_mat_data = pd.read_csv('data/mat_data.csv', index_col=0)
df_SMs = pd.read_csv('data/SM_data.csv', index_col=0)

#TODO: figure out how to deal with duplicate SM (i.e physical properties). 
# Also removed duplicate SM (with different electrolytes from choi 2015)
# df_SMs = df_SMs.where(df_SMs['source'] != 'Alok 2021').dropna(subset=['source'])

#%%

mats = df_SMs['materials']
mats_single = mats.where(~mats.str.contains('[', regex=False)).dropna()

# present_mats = [m for m in mats_single if m in df_mat_data.index]
missing_mats = [m for m in mats_single if m not in df_mat_data.index]

print("missing single materials: {}".format(missing_mats))

SP_single = [df_mat_data['specific_price'][m] if m in df_mat_data.index else np.nan for m in mats_single]
mu_totals_single = [df_mat_data['mu'][m] if m in df_mat_data.index else np.nan for m in mats_single]
price_sources = [df_mat_data['sources'][m] if m in df_mat_data.index else np.nan for m in mats_single]


df_single = pd.DataFrame({
    'specific_price': SP_single,
    'mu_total': mu_totals_single,
    'price_sources': price_sources
    }, index= mats_single.index)


SP_single = pd.Series(SP_single, index=mats_single.index)
SP_single


#%%


import ast

mats_comp = mats.where(mats.str.contains('[', regex=False)).dropna()
mats_comp = mats_comp.apply(ast.literal_eval)
mats_comp
#%%
specific_prices = []
mu_totals = []
price_sources = []
for mat_list in mats_comp:
    mus = []
    molar_prices = []
    price_sources_mat = []
    total_mole_fractions = 0 #Used to normalize mole fractions to 1 at the end

    missing_price_data = False

    for i, (mat_index, mole_fraction) in enumerate(mat_list):
        if mat_index not in df_mat_data.index:
            print('missing: {}'.format(mat_index))
            missing_price_data = True
            continue

        total_mole_fractions += mole_fraction

        sp = df_mat_data['specific_price'][mat_index]
        mu = df_mat_data['mu'][mat_index]
        price_source = '{} : {}'.format(i, df_mat_data['sources'][mat_index])

        #really molar prices weighted by mole fraciton
        molar_price = mole_fraction*sp*mu*1000 #($/kg * g/mol * kg/g)
        
        mus.append(mu)
        molar_prices.append(molar_price)
        price_sources_mat.append(price_source)

    if not missing_price_data:
        price_sources.append(", ".join(price_sources_mat))

        mu_total = sum(mus)
        mu_totals.append(mu_total)

        specific_price = sum(molar_prices)/(total_mole_fractions*mu_total*1000)
        specific_prices.append(specific_price)
    else:
        price_sources.append('missing')
        mu_totals.append(np.nan)
        specific_prices.append(np.nan)



df_comp = pd.DataFrame({
    'specific_price': specific_prices,
    'mu_total': mu_totals,
    'price_sources':price_sources
    }, index= mats_comp.index)


#%%

df_all = pd.concat([df_single, df_comp])
df_all
#%%

#TODO: can't assign by index because of duplicate SM indexes. Mainly two latent datasets alva and alok.
df_SMs['specific_price'] = df_all['specific_price']
df_SMs['mu_total'] = df_all['mu_total']
df_SMs['price_sources'] = df_all['price_sources']







#%%


sensible_thermal = (df_SMs['Cp']*500)
sensible_thermal.name='specific_energy'
sensible_thermal = sensible_thermal.to_frame()
# sensible_thermal['energy_type'] = 'Thermal (Sensible)'

# sensible_thermal.dropna()

#%%

latent_thermal = (df_SMs['sp_latent_heat'])
latent_thermal.name='specific_energy'
latent_thermal = latent_thermal.to_frame()
# latent_thermal['energy_type'] = 'Thermal (Latent)'

thermochem = (df_SMs['deltaH_thermochem'])
thermochem.name='specific_energy'
thermochem = thermochem.to_frame()
# thermochem['energy_type'] = 'Chemical (Thermochemical)'

chemical = (df_SMs['deltaG_chem'])
chemical.name='specific_energy'
chemical = chemical.to_frame()
# chemical['energy_type'] = 'Chemical (Syn. fuel)'


#TODO: deltaV means battery deltaV
F = 96485 # C/mol
electrochemical = (1/3600)*F*df_SMs['deltaV']/df_SMs['mu_total']
electrochemical.name='specific_energy'
electrochemical = electrochemical.to_frame()
# electrochemical['energy_type'] = 'Chemical (Battery)'


virial = (df_SMs['specific_strength']/3600) #TODO:Assuming Q=1
virial.name='specific_energy'
virial = virial.to_frame()
# virial['energy_type'] = 'Viral Limited'


epsilon_0 = 8.85e-12
def calc_electrostatic_SE(V_breakdown, dielectric_const, rho_m):
    specific_energy = 0.5*(V_breakdown**2)*dielectric_const*epsilon_0 #J/m3
    specific_energy = specific_energy/(rho_m) #J/kg
    specific_energy = specific_energy/3600000 #kWh/kg
    return specific_energy

electrostatic = calc_electrostatic_SE(
    V_breakdown=df_SMs['dielectric_breakdown'],
    dielectric_const=df_SMs['dielectric_constant'],
    rho_m = df_SMs['mass_density']
)
electrostatic.name='specific_energy'
electrostatic = electrostatic.to_frame()
# electrostatic['energy_type'] = 'Electrostatic (Capacitor)'


#TODO: need to implement pseudocapactior. As well as make deltaV work with batteries
electrostatic_edlc = (0.5*df_SMs['specific_capacitance']*df_SMs['deltaV_electrolyte']**2) #J/g
electrostatic_edlc = electrostatic_edlc/3600

electrostatic_edlc.name='specific_energy'
electrostatic_edlc = electrostatic_edlc.to_frame()
# electrostatic_edlc['energy_type'] = 'Electrostatic (EDLC)'



gravitational = (df_SMs['delta_height']*9.81/3600000)
gravitational.name='specific_energy'
gravitational = gravitational.to_frame()
# gravitational['energy_type'] = 'Gravitational'

dfs = [
    chemical,
    thermochem,
    electrochemical,
    sensible_thermal,
    latent_thermal,
    virial,
    electrostatic_edlc,
    electrostatic,
    gravitational
]


dfs_2 = []

#TODO: improve
columns_keep = ['mu_total','specific_price','price_sources', 'SM_sources','SM_type']
for df in dfs:
    for col in columns_keep:
        df[col] = df_SMs[col]
    dfs_2.append(df)

df_out = pd.concat(dfs_2).dropna(subset=['specific_energy'])

df_out['C_kwh'] = df_out['specific_price']/df_out['specific_energy']

# df_out = df_out.dropna(subset=['C_kwh'])

# %%

df_out.to_csv('data/C_kwh.csv')

# %%
