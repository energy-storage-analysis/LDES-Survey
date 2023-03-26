#%%
import os
if not os.path.exists('output'): os.mkdir('output')

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({
    "savefig.facecolor": 'white',
    "font.size": 7, 
    'savefig.dpi': 600, 
    'font.sans-serif': 'arial', 
    'figure.figsize': (2.3, 2.5)
})


# %%

from lcos_fns import calc_lcos, gen_legend_figure

CF = 0.7
eta_RTs = [1,0.75,0.5]


eta_linestyles = ['-','--','-.']
eta_linestyle_dict = {eta: eta_linestyles[i] for i, eta in enumerate(eta_RTs)}


legendFig = gen_legend_figure(eta_linestyle_dict, title='$\eta_{RT}$', style_type='linestyle')
legendFig.savefig('output/legend_eta.png', transparent=True)


C_kWhs = [10,100,1000]
DD = np.logspace(np.log10(1),np.log10(300), num=100),

C_Ein = 0.05
C_kW = 100
LT = 10


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
LT = 10,
)

da_lcos = calc_lcos.run_combos(combos, constants=constants)['lcos']
da_lcos.attrs = dict(long_name='LCOS', units='USD/kWh')
da_lcos.coords['DD'].attrs = dict(long_name='Discharge Duration', units='h')

da_lcos

# %%

da_lcos_stack = da_lcos.stack(temp = ['C_kWh', 'eta_RT'])

colors = ['purple','g','b']
color_dict = {eta: colors[i] for i, eta in enumerate(da_lcos.coords['C_kWh'].values)}


legendFig = gen_legend_figure(color_dict, title='$C_{kWh} [\\frac{USD}{kWh}]$', style_type='color')
legendFig.savefig('output/legend_Ckwh.png', transparent=True)


plt.figure()

for C_kWh, eta_RT in da_lcos_stack.coords['temp'].values:
    da_lcos.sel(C_kWh=C_kWh, eta_RT=eta_RT).plot(
        linestyle=eta_linestyle_dict[eta_RT],
        linewidth=1,
        color=color_dict[C_kWh],
        label='$C_{{kWh}}$: {} USD/kWh, $\eta_{{RT}}$: {}'.format(C_kWh,eta_RT)
    )


plt.gca().set_title('')
plt.xscale('log')
plt.yscale('log')
# plt.legend(bbox_to_anchor=[0,0,1.8,1])
plt.tight_layout()

plt.savefig('output/LCOS_Duraiton_pub.png')

# %%
