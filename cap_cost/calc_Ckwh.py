#%%
from cgitb import lookup
import os
from os.path import join as pjoin
import numpy as np
import pandas as pd

df_mat_data = pd.read_csv('data_consolidated/mat_data.csv', index_col=0)
df_SMs = pd.read_csv('data_consolidated/SM_data.csv', index_col=[0,1])


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
mats_comp_basis = df_SMs['mat_basis'][mats_comp.index]

df_mats_comp = pd.concat([mats_comp,mats_comp_basis], axis=1)

df_mats_comp['specific_price'] = np.nan
df_mats_comp['mu_total'] = np.nan
df_mats_comp['price_sources'] = ''


print("Calculating composite material data")

for mat_idx, row in df_mats_comp.iterrows():
    mus = []
    price_components = []
    price_sources_mat = []

    missing_prices = []

    mat_list = row['materials']
    mat_basis = row['mat_basis']

    for i, (mat_index, fraction) in enumerate(mat_list):
        if mat_index not in df_mat_data.index:
            missing_prices.append(mat_index)
            continue

        specific_price = df_mat_data['specific_price'][mat_index]

        mu = df_mat_data['mu'][mat_index]
        mus.append(mu)
        price_source = '{} : {}'.format(i, df_mat_data['sources'][mat_index])
        price_sources_mat.append(price_source)

        if mat_basis == 'molar':
            molar_price = specific_price*mu*1000 #($/kg * g/mol * kg/g)
            price_components.append(molar_price*fraction)
        elif mat_basis == 'mass':
            price_components.append(specific_price*fraction)
        else:
            raise ValueError("Incorrect mat_basis for {}, must be 'molar' or 'mass'".format(mat_idx))

    mu_total = sum(mus)
    df_mats_comp.loc[mat_idx, 'mu_total'] = mu_total

    if len(missing_prices) == 0:
        df_mats_comp.loc[mat_idx, 'price_sources'] = ", ".join(price_sources_mat)

        if mat_basis == 'molar':
            specific_price = sum(price_components)/(mu_total*1000)
        elif mat_basis == 'mass':
            specific_price = sum(price_components)

        df_mats_comp.loc[mat_idx, 'specific_price'] = specific_price
    else:
        print('missing material prices {} for {}'.format(missing_prices, mat_idx))

df_mats_comp


#%%

df_all = pd.concat([df_single, df_mats_comp])
df_all
#%%

df_SMs['specific_price'] = df_all['specific_price']
df_SMs['mu_total'] = df_all['mu_total']
df_SMs['price_sources'] = df_all['price_sources']

#%%

sensible_thermal = (df_SMs['Cp']*df_SMs['deltaT'])
sensible_thermal.name='specific_energy'
sensible_thermal = sensible_thermal.to_frame()

#%%

latent_thermal = (df_SMs['sp_latent_heat'])
latent_thermal.name='specific_energy'
latent_thermal = latent_thermal.to_frame()

thermochem = (df_SMs['deltaH_thermochem'])
thermochem.name='specific_energy'
thermochem = thermochem.to_frame()

chemical = (df_SMs['deltaG_chem'])/(df_SMs['mu_total']/1000)
chemical.name='specific_energy'
chemical = chemical.to_frame()

F = 96485 # C/mol
#TODO: deltaV means battery deltaV
electrochemical = (1/3600)*F*df_SMs['deltaV']/df_SMs['mu_total']
electrochemical.name='specific_energy'
electrochemical = electrochemical.to_frame()


virial = (df_SMs['specific_strength']/3600) #TODO:Assuming Q=1
virial.name='specific_energy'
virial = virial.to_frame()


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


#TODO: need to implement pseudocapactior. As well as make deltaV work with batteries
electrostatic_edlc = (0.5*df_SMs['specific_capacitance']*df_SMs['deltaV_electrolyte']**2) #J/g
electrostatic_edlc = electrostatic_edlc/3600

electrostatic_edlc.name='specific_energy'
electrostatic_edlc = electrostatic_edlc.to_frame()



gravitational = (df_SMs['delta_height']*9.81/3600000)
gravitational.name='specific_energy'
gravitational = gravitational.to_frame()

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
columns_keep = ['mu_total','specific_price','price_sources', 'SM_sources']
for df in dfs:
    for col in columns_keep:
        df[col] = df_SMs[col]
    dfs_2.append(df)

df_out = pd.concat(dfs_2).dropna(subset=['specific_energy'])

df_out['C_kwh'] = df_out['specific_price']/df_out['specific_energy']

# df_out = df_out.dropna(subset=['C_kwh'])

# %%

df_out.to_csv('data_consolidated/C_kwh.csv')

# %%
df_sel = df_out.where(df_out['C_kwh'] < 10).dropna(how='all')

df_sel = df_sel[['specific_energy','specific_price','price_sources','SM_sources','C_kwh']]

df_sel.sort_values('C_kwh').to_csv('analysis/output/SM_downselected.csv')
