import sys
sys.path.append('..')

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({
    "savefig.facecolor": 'white',
    "font.size": 7, 
    'savefig.dpi': 600, 
    'font.sans-serif': 'arial', 
    'figure.figsize': (2.3, 2.5)
})

from lcos_fns import calc_CkW_max, gen_legend_figure


CF = 0.7
eta_RTs = [1,0.75,0.5]
eta_linestyles = ['-','--','-.']
eta_linestyle_dict = {eta: eta_linestyles[i] for i, eta in enumerate(eta_RTs)}

combos = dict(
DD = [100,10, 1],
C_kWh = np.logspace(np.log10(1), np.log10(1000), num=500),
eta_RT = eta_RTs
)

constants = dict(
LCOS_set = 0.05,
C_Ein = 0.05,
LT = 10,
CF = 0.7 #Albertus says '70% of max cycles'
)

da_CkW = calc_CkW_max.run_combos(combos, constants=constants)['C_kW']
da_CkW.coords['DD'].attrs = dict(long_name='Discharge Duration', units='h')
# da

#%%


da_CkW_stack = da_CkW.stack(temp = ['DD', 'eta_RT'])


# colors = ['tab:purple','tab:orange','tab:brown']
colors = ['c', 'y', 'k']
color_dict = {eta: colors[i] for i, eta in enumerate(da_CkW.coords['DD'].values)}


legendFig = gen_legend_figure(color_dict, title='$DD [h]$', style_type='color')
legendFig.savefig('output/legend_DD.png', transparent=True)



plt.figure()

for DD, eta_RT in da_CkW_stack.coords['temp'].values:
    da_CkW.sel(DD=DD, eta_RT=eta_RT).plot(
        linestyle=eta_linestyle_dict[eta_RT],
        color=color_dict[DD],
        label='$DD$: {} h, $\eta_{{RT}}$: {}'.format(DD,eta_RT)

    )

plt.xlabel('$C_{kWh}$ (USD/kWh)')
plt.ylim(1e2,1e4)
plt.xticks([1e0,1e1,1e2,1e3])

plt.gca().set_title('')
plt.xscale('log')
plt.yscale('log')
# plt.legend(bbox_to_anchor=[0,0,1.8,1])

plt.ylabel('Maximum $C_{kW}$ (USD/kW)')
plt.tight_layout()

plt.savefig('output/EP_capitaltradeoff_pub.png')
# %%

# %%
