#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import xyzpy

plt.rcParams.update({
    "savefig.facecolor": 'white',
    "font.size": 14
})
# %%



#%%

@xyzpy.label(var_names=['CF'])
def calc_CF(num_cycles_year, DD):
    CF = num_cycles_year*(DD/8760)
    if CF > 1:
        return np.nan
    else:
        return CF


combos = dict(
DD = np.logspace(np.log2(1),np.log2(1024), base=2, num=500),
num_cycles_year = np.logspace(np.log10(1),np.log10(10000), base=10, num=500),
)

da_CF = calc_CF.run_combos(combos)['CF']
da_CF.coords['DD'].attrs = dict(long_name='Discharge Duration', units='h')
da_CF.coords['num_cycles_year'].attrs = dict(long_name='Num. Cyc. Year')
#%%

plt.figure()

da_CF.plot(norm=mpl.colors.LogNorm())
plt.xscale('log')
plt.yscale('log')

plt.suptitle('Capacity Factor')

plt.savefig('output/CF_2D_fig.png')

#%%


@xyzpy.label(var_names=['lcos'])
def calc_lcos(DD, CF, C_Ein, eta, C_kW, C_kWh, LT):
    elec_premium = C_Ein*((1/eta)-1)

    capital_term_dem = C_kW + C_kWh*DD
    capital_term_num = LT*8760*CF*eta 
    capital_term = capital_term_dem/capital_term_num

    lcos= elec_premium + capital_term
    return lcos

@xyzpy.label(var_names=['lcos'])
def calc_lcos_ncy(DD, num_cycles_year, C_Ein, eta, C_kW, C_kWh, LT):
    CF = calc_CF(num_cycles_year, DD)
    lcos = calc_lcos(DD, CF, C_Ein, eta, C_kW, C_kWh, LT)
    return lcos

constants = dict(
C_Ein = 0.05,
eta = 0.8,
C_kW = 100,
C_kWh = 50,
LT = 20,
)

da_lcos = calc_lcos_ncy.run_combos(combos, constants=constants)['lcos']
# %%
plt.figure()

da_lcos.plot(norm=mpl.colors.LogNorm())
plt.xscale('log')
plt.yscale('log')

plt.suptitle('LCOS ($/kWh)')

plt.savefig('output/LCOS_2D_CF_fig.png')
# %%

combos = dict(
DD = np.logspace(np.log2(1),np.log2(1024), base=2, num=500),
CF = np.linspace(0.1,1,5),
)

constants = dict(
C_Ein = 0.05,
eta = 0.8,
C_kW = 100,
C_kWh = 50,
LT = 20,
)

da_lcos = calc_lcos.run_combos(combos, constants=constants)['lcos']

#%%
plt.figure()
da_lcos.plot(hue='CF')
plt.xscale('log')
plt.yscale('log')

plt.xlabel('Discharge Duration')
plt.ylabel('LCOS ($/kWh)')
plt.ylim(0.01,5)
# plt.legend(title='Capacity Factor')

plt.savefig('output/LCOS_CF_fig.png')
#%%

@xyzpy.label(var_names=['C_kW'])
def calc_CkW_max(DD, C_kWh, eta, LT, C_Ein, LCOS_set):
    C_kW = LT*8760*eta*( LCOS_set - ( (1/eta)-1 )*C_Ein ) - C_kWh*DD
    return C_kW


combos = dict(
DD = [round(n,3) for n in np.logspace(np.log10(1), np.log10(300), 5)],
C_kWh = np.logspace(np.log10(1), np.log10(1000), num=500)
)

constants = dict(
LCOS_set = 0.05,
C_Ein = 0.05,
eta = 0.8,
LT = 20,
)

da = calc_CkW_max.run_combos(combos, constants=constants)['C_kW']
da

#%%


plt.figure()
da.plot(hue='DD')
plt.yscale('log')
plt.xscale('log')

plt.xlabel('Energy Capital Cost ($/kWh)')
plt.ylabel('Power Capital Cost ($/kW)')

plt.savefig('output/EP_capitaltradeoff.png')