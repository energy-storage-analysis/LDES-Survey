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

#4380 max cycles following Albertus
@xyzpy.label(var_names=['CF'])
def calc_CF(num_cycles_year, DD):
    CF = num_cycles_year*(DD/4380)
    if CF > 1:
        return np.nan
    else:
        return CF

@xyzpy.label(var_names=['DD'])
def calc_DD_from_CF(num_cycles_year, CF):
    DD = CF*(4380/num_cycles_year)
    return DD

combos = dict(
DD = np.logspace(np.log2(1),np.log2(1024), base=2, num=500),
num_cycles_year = np.logspace(np.log10(1),np.log10(4380), base=10, num=500),
)

da_CF = calc_CF.run_combos(combos)['CF']
da_CF.coords['DD'].attrs = dict(long_name='Discharge Duration', units='h')
da_CF.coords['num_cycles_year'].attrs = dict(long_name='Num. Cyc. Year')

CFs_fixed = np.linspace(0.1,1,4)
#%%

plt.figure()

da_CF.plot(norm=mpl.colors.LogNorm())
plt.xscale('log')
plt.yscale('log')

for CF in CFs_fixed:
    DDs_CF_fixed = calc_DD_from_CF(combos['num_cycles_year'], CF)
    plt.plot(combos['num_cycles_year'],DDs_CF_fixed)

plt.suptitle('Capacity Factor')

plt.tight_layout()

plt.savefig('output/CF_2D_fig.png')

#%%


@xyzpy.label(var_names=['lcos'])
def calc_lcos(DD, CF, C_Ein, eta_RT, C_kW, C_kWh, LT):
    elec_premium = C_Ein*((1/eta_RT)-1)

    capital_term_dem = C_kW + C_kWh*DD
    capital_term_num = LT*4380*CF*np.sqrt(eta_RT) 
    capital_term = capital_term_dem/capital_term_num

    lcos= elec_premium + capital_term
    return lcos

@xyzpy.label(var_names=['lcos'])
def calc_lcos_ncy(DD, num_cycles_year, C_Ein, eta_RT, C_kW, C_kWh, LT):
    CF = calc_CF(num_cycles_year, DD)
    lcos = calc_lcos(DD, CF, C_Ein, eta_RT, C_kW, C_kWh, LT)
    return lcos

#%%


constants = dict(
C_Ein = 0.05,
eta_RT = 0.8,
C_kW = 100,
C_kWh = 100,
LT = 10,
)

da_lcos = calc_lcos_ncy.run_combos(combos, constants=constants)['lcos']


# %%
plt.figure()

da_lcos.plot(norm=mpl.colors.LogNorm())
plt.xscale('log')
plt.yscale('log')

plt.suptitle('LCOS ($/kWh)')

for CF in CFs_fixed:
    DDs_CF_fixed = calc_DD_from_CF(combos['num_cycles_year'], CF)
    plt.plot(combos['num_cycles_year'],DDs_CF_fixed)

plt.tight_layout()

plt.savefig('output/LCOS_2D_CF_fig.png')
# %%

combos = dict(
DD = np.logspace(np.log10(1),np.log10(300), num=100),
C_kWh = np.logspace(0,4,5),
CF = CFs_fixed,
eta_RT = np.linspace(0.3,0.9,4)
)

constants = dict(
C_Ein = 0.05,
C_kW = 100,
LT = 20,
)

da_lcos = calc_lcos.run_combos(combos, constants=constants)['lcos']
da_lcos.attrs = dict(long_name='LCOS', units='$/kWh')
da_lcos.coords['DD'].attrs = dict(long_name='Discharge Duration', units='h')
da_lcos.coords['CF'].attrs = dict(long_name='Capacity Factor')
da_lcos
#%%
plt.figure()
da_lcos.sel(C_kWh=10, eta_RT =0.8, method='nearest').plot(hue='CF')
plt.xscale('log')
plt.yscale('log')

# plt.ylim(0.01,5)

plt.tight_layout()

plt.savefig('output/LCOS_CF_fig.png')
#%%




#%%

plt.figure()
da_lcos.sel(CF=1).plot(col='eta_RT', hue='C_kWh', yscale='log',xscale='log')#, norm=mpl.colors.LogNorm())

plt.savefig('output/LCOS_Duration.png')
#%%

@xyzpy.label(var_names=['C_kW'])
def calc_CkW_max(DD, C_kWh, eta_RT, LT, CF, C_Ein, LCOS_set):
    eta_d = np.sqrt(eta_RT)
    C_kW = LT*4380*CF*eta_d*( LCOS_set - ( (1/eta_RT)-1 )*C_Ein ) - C_kWh*DD
    return C_kW


combos = dict(
# DD = [round(n,3) for n in np.logspace(np.log10(1), np.log10(300), 5)],
DD = [1,3,10,30,100],
C_kWh = np.logspace(np.log10(1), np.log10(1000), num=500),
eta_RT = np.linspace(0.4,1,4)
)

constants = dict(
LCOS_set = 0.1,
C_Ein = 0.05,
LT = 10,
CF = 0.7 #Albertus says '70% of max cycles'
)

da = calc_CkW_max.run_combos(combos, constants=constants)['C_kW']
da.coords['DD'].attrs = dict(long_name='Discharge Duration', units='h')
# da

#%%


plt.figure()
g = da.plot(hue='DD', col='eta_RT', xscale='log',yscale='log')

for ax in g.axes.flatten():
    ax.set_xlabel('Energy Capital Cost ($/kWh)')
    ax.set_ylim(1e2,1e4)
    ax.set_xticks([1e0,1e1,1e2,1e3])

g.axes[0][0].set_ylabel('Power Capital Cost ($/kW)')

plt.savefig('output/EP_capitaltradeoff.png')
# %%

# %%
