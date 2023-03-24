#%%
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

plt.rcParams.update({
    "savefig.facecolor": 'white',
    "font.size": 14
})

#%%

from lcos_fns import calc_CF

combos = dict(
DD = np.logspace(np.log2(1),np.log2(1024), base=2, num=500),
num_cycles_year = np.logspace(np.log10(1),np.log10(4380), base=10, num=500),
)

da_CF = calc_CF.run_combos(combos)['CF']
da_CF.coords['DD'].attrs = dict(long_name='Discharge Duration', units='h')
da_CF.coords['num_cycles_year'].attrs = dict(long_name='Num. Cyc. Year')

CFs_fixed = np.linspace(0.1,1,4)
#%%

from lcos_fns import calc_DD_from_CF

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
from lcos_fns import calc_lcos_ncy

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

from lcos_fns import calc_lcos

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

plt.figure()
da_lcos.sel(CF=1).plot(col='eta_RT', hue='C_kWh', yscale='log',xscale='log')#, norm=mpl.colors.LogNorm())

plt.savefig('output/LCOS_Duration.png')
#%%
from lcos_fns import calc_CkW_max

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