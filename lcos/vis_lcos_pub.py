#%%
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from sympy import O

plt.rcParams.update({
    "savefig.facecolor": 'white',
    "font.size": 14
})
# %%

from lcos_fns import calc_lcos

CF = 0.7
eta_RTs = [1,0.5]


eta_linestyles = ['-','--','-.']
eta_linestyle_dict = {eta: eta_linestyles[i] for i, eta in enumerate(eta_RTs)}


C_kWhs = [10,100,1000]
DD = np.logspace(np.log10(1),np.log10(300), num=100),

C_Ein = 0.05
C_kW = 100
LT = 20


#%%
 
from lcos_fns import calc_lcos

combos = dict(
DD = np.logspace(np.log10(1),np.log10(300), num=100),
C_kWh = [10,100,1000],
eta_RT = eta_RTs
)

constants = dict(
CF = 0.7,
C_Ein = 0.05,
C_kW = 1000,
LT = 20,
)

da_lcos = calc_lcos.run_combos(combos, constants=constants)['lcos']
da_lcos.attrs = dict(long_name='LCOS', units='$/kWh')
da_lcos.coords['DD'].attrs = dict(long_name='Discharge Duration', units='h')

da_lcos

# %%
plt.figure(figsize=(15,4))

da_lcos_stack = da_lcos.stack(temp = ['C_kWh', 'eta_RT'])

colors = ['r','g','b']
color_dict = {eta: colors[i] for i, eta in enumerate(da_lcos.coords['C_kWh'].values)}

for C_kWh, eta_RT in da_lcos_stack.coords['temp'].values:
    da_lcos.sel(C_kWh=C_kWh, eta_RT=eta_RT).plot(
        linestyle=eta_linestyle_dict[eta_RT],
        color=color_dict[C_kWh],
        label='$C_{{kWh}}$: {} \$/kWh, $\eta_{{RT}}$: {}'.format(C_kWh,eta_RT)
    )


plt.gca().set_title('')
plt.xscale('log')
plt.yscale('log')
plt.legend(bbox_to_anchor=[0,0,1.8,1])
plt.tight_layout()

plt.savefig('output/LCOS_Duraiton_pub.png')

# %%

from lcos_fns import calc_CkW_max

combos = dict(
DD = [100,10, 1],
C_kWh = np.logspace(np.log10(1), np.log10(1000), num=500),
eta_RT = eta_RTs
)

constants = dict(
LCOS_set = 0.1,
C_Ein = 0.05,
LT = 10,
CF = 0.7 #Albertus says '70% of max cycles'
)

da_CkW = calc_CkW_max.run_combos(combos, constants=constants)['C_kW']
da_CkW.coords['DD'].attrs = dict(long_name='Discharge Duration', units='h')
# da

#%%

plt.figure(figsize=(6,4))

da_CkW_stack = da_CkW.stack(temp = ['DD', 'eta_RT'])


colors = ['tab:purple','tab:orange','tab:brown']
color_dict = {eta: colors[i] for i, eta in enumerate(da_CkW.coords['DD'].values)}

for DD, eta_RT in da_CkW_stack.coords['temp'].values:
    da_CkW.sel(DD=DD, eta_RT=eta_RT).plot(
        linestyle=eta_linestyle_dict[eta_RT],
        color=color_dict[DD],
        # label='$DD$: {} h, $\eta_{{RT}}$: {}'.format(DD,eta_RT)

    )

plt.xlabel('Energy Capital ($/kWh)')
plt.ylim(1e2,1e4)
plt.xticks([1e0,1e1,1e2,1e3])

plt.gca().set_title('')
plt.xscale('log')
plt.yscale('log')
# plt.legend(bbox_to_anchor=[0,0,2,1])

plt.ylabel('Maximum Power Capital ($/kW)')
plt.tight_layout()

plt.savefig('output/EP_capitaltradeoff_pub.png')
# %%

# %%
