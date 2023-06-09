#%%
import numpy as np
import pandas as pd
from es_utils.units import prep_df_pint_out, read_pint_df, ureg

df_mat_data = read_pint_df('data_consolidated/mat_data.csv')
df_SMs =  read_pint_df('data_consolidated/SM_data.csv', index_col=[0,1])

#%%

mats = df_SMs['materials']
mats_single = mats.where(~mats.str.contains('[', regex=False)).dropna()

# present_mats = [m for m in mats_single if m in df_mat_data.index]
missing_mats = [m for m in mats_single if m not in df_mat_data.index]

print("missing single materials: {}".format(missing_mats))

SP_single = [df_mat_data['specific_price'][m] if m in df_mat_data.index else np.nan for m in mats_single]
mu_totals_single = [df_mat_data['mu'][m] if m in df_mat_data.index else np.nan for m in mats_single]
price_sources = [df_mat_data['sources'][m] if m in df_mat_data.index else np.nan for m in mats_single]

#Assuming all volumetric storage media are based on a signle volumetric price 
vol_single = [df_mat_data['vol_price'][m] if m in df_mat_data.index else np.nan for m in mats_single]

df_single = pd.DataFrame({
    'specific_price': SP_single,
    'vol_price': vol_single,
    'mu_total': mu_totals_single,
    'price_sources': price_sources
    }, index= mats_single.index)

#Not exactly sure why I have to set these again. 
df_single = df_single.astype({
    'specific_price' : 'pint[USD/kg]',
    'vol_price': 'pint[USD/m**3]',
    'mu_total': 'pint[g/mol]'
})

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

mu_totals = [] #Having to build a list vs location indexing because of pint...
specific_prices = []

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
        price_source = '{} : {}'.format(i, df_mat_data['sources'][mat_index])
        price_sources_mat.append(price_source)

        if mat_basis == 'molar':
            molar_price = specific_price*mu #($/kg * g/mol * kg/g)
            price_components.append(molar_price*fraction)
            mus.append(mu*fraction)
        elif mat_basis == 'mass':
            price_components.append(specific_price*fraction)
            mus.append(np.nan) #TODO: how to calculate total molar mass of compoents specified by mass fraciton? IS total molar mass well defined? 
        else:
            raise ValueError("Incorrect mat_basis for {}, must be 'molar' or 'mass'".format(mat_idx))

    mu_total = sum(mus)
    mu_totals.append(mu_total)

    if len(missing_prices) == 0:
        df_mats_comp.loc[mat_idx, 'price_sources'] = ", ".join(price_sources_mat)

        if mat_basis == 'molar':
            specific_price = sum(price_components)/(mu_total)
        elif mat_basis == 'mass':
            specific_price = sum(price_components)

        # df_mats_comp.loc[mat_idx, 'specific_price'] = specific_price.magnitude
        specific_prices.append(specific_price)
    else:
        specific_prices.append(specific_price)
        print('missing material prices {} for {}'.format(missing_prices, mat_idx))



df_mats_comp['mu_total'] = mu_totals
df_mats_comp['mu_total'] = df_mats_comp['mu_total'].replace(0, np.nan) #Materials with all missing prices have 0 mu_total...
df_mats_comp['mu_total'] = df_mats_comp['mu_total'].astype('pint[g/mol]')
df_mats_comp['specific_price'] = specific_prices
df_mats_comp['specific_price'] = df_mats_comp['specific_price'].astype('pint[USD/kg]')


df_mats_comp


#%%

df_all = pd.concat([df_single, df_mats_comp])
df_all
#%%

df_SMs['specific_price'] = df_all['specific_price']
df_SMs['vol_price'] = df_all['vol_price']

#We allow mu_total to be defined up front, so only replace if it doesn't exist already
#TODO: This is needed because we are forcing volumetric calculations into the mass calculation pipeline. 
df_SMs['mu_total'].loc[df_all['mu_total'].dropna().index] = df_all['mu_total'].dropna()

df_SMs['price_sources'] = df_all['price_sources']
#%%

#Calculate the specific price of the storage media with volumetric costs, needs to be done here to have the mass density of the storage medium. 
specific_price_vol = df_SMs['vol_price']/df_SMs['mass_density']
specific_price_vol = specific_price_vol.dropna()

df_SMs['specific_price'].loc[specific_price_vol.index] = specific_price_vol
df_SMs['mat_basis'].loc[specific_price_vol.index] = 'volumetric'

df_SMs = df_SMs.drop('vol_price', axis=1)


#%%

# Energy density expressions


F = ureg.Quantity(96485, 'C/mol') # C/mol
#TODO: deltaV means battery deltaV
electrochemical = F*df_SMs['n_e']*df_SMs['deltaV']/df_SMs['mu_total']
electrochemical.name='specific_energy'
electrochemical = electrochemical.to_frame()

chemical = df_SMs['deltaG_chem']/df_SMs['mu_total']
chemical.name='specific_energy'
chemical = chemical.to_frame()

#TODO: need to implement pseudocapactior. As well as make deltaV work with batteries
electrostatic_edlc = (0.5*df_SMs['specific_capacitance']*df_SMs['deltaV_cap']**2) #J/g
electrostatic_edlc.name='specific_energy'
electrostatic_edlc = electrostatic_edlc.to_frame()

thermochem = df_SMs['deltaH_thermochem']
thermochem.name='specific_energy'
thermochem = thermochem.to_frame()

sensible_thermal = df_SMs['Cp']*df_SMs['deltaT']
sensible_thermal.name='specific_energy'
sensible_thermal = sensible_thermal.to_frame()

latent_thermal = df_SMs['sp_latent_heat']
latent_thermal.name='specific_energy'
latent_thermal = latent_thermal.to_frame()

pressure = df_SMs['P_cavern']/df_SMs['mass_density']
pressure.name='specific_energy'
pressure = pressure.to_frame()

virial = df_SMs['specific_strength']/df_SMs['Qmax']
virial.name='specific_energy'
virial = virial.to_frame()

accel_g = ureg.Quantity(9.81, 'm/s**2')
gravitational = df_SMs['delta_height']*accel_g
gravitational.name='specific_energy'
gravitational = gravitational.to_frame()

epsilon_0 = ureg.Quantity(8.85e-12, 'F/m')
def calc_electrostatic_SE(V_breakdown, dielectric_const, rho_m):
    specific_energy = 0.5*(V_breakdown**2)*dielectric_const*epsilon_0 #J/m3
    specific_energy = specific_energy/(rho_m) #J/kg
    return specific_energy

electrostatic = calc_electrostatic_SE(
    V_breakdown=df_SMs['dielectric_breakdown'],
    dielectric_const=df_SMs['dielectric_constant'],
    rho_m = df_SMs['mass_density']
)
electrostatic.name='specific_energy'
electrostatic = electrostatic.to_frame()


dfs = [
    chemical,
    thermochem,
    electrochemical,
    sensible_thermal,
    pressure,
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

df_out['specific_energy'] = df_out['specific_energy'].astype('pint[kWh/kg]')

df_out['C_kwh'] = df_out['specific_price']/df_out['specific_energy']

df_out = df_out.dropna(subset=['C_kwh'])
df_out['C_kwh'] = df_out['C_kwh'].astype('pint[USD/kWh]')


# %%

#Drop columns in df_SMs so that duplicate columns don't keep getting added when rerunning this script without rerunning consolidate data. I.e. we are writing or overwriting the values.
df_SMs = df_SMs[[col for col in df_SMs.columns if col not in df_out.columns]]

df_SMs = pd.concat([df_SMs, df_out], axis=1)


# Column order 
first_columns = ['sub_type','mat_type','C_kwh','specific_energy','specific_price','materials','mat_basis', 'SM_sources','price_sources']
other_cols = sorted([col for col in df_SMs.columns if col not in first_columns])
columns = [*first_columns, *other_cols]
df_SMs = df_SMs[columns]

df_SMs = prep_df_pint_out(df_SMs)

df_SMs.to_csv('data_consolidated/SM_data.csv')

# %%
