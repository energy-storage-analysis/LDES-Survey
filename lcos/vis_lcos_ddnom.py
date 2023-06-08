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
    'figure.figsize': (2.3, 3)
})

# Fixed constants between plots. 
C_Ein = 0.011 #Taken from https://www.eia.gov/electricity/state/
CF = 0.5
LT = 10


# %%

from lcos_fns import calc_lcos
from es_utils.plot import gen_legend_figure

DD_noms = [10]
C_kWhs = [1, 10,100]
DDs = np.logspace(np.log10(1),np.log10(300), num=100)

constants = dict(
CF = CF,
C_Ein = C_Ein, 
C_kW = 75,
LT = LT,
eta_RT = 0.85
)




#%%
 
from lcos_fns import calc_lcos_DD_nom

combos = dict(
DD = DDs,
C_kWh = C_kWhs,
DD_nom = DD_noms,
coupling = ['coupled','decoupled']
)


da_lcos = calc_lcos_DD_nom.run_combos(combos, constants=constants)['lcos']
da_lcos.attrs = dict(long_name='LCOS', units='USD/kWh')
da_lcos.coords['DD'].attrs = dict(long_name='Discharge Duration', units='h')

da_lcos

# %%


linestyles = ['-','--','-.']
linestyle_dict = {DD_nom: linestyles[i] for i, DD_nom in enumerate(DD_noms)}


legendFig = gen_legend_figure(linestyle_dict, title='$DD_{nom}$', style_type='linestyle')
legendFig.savefig('output/legend_linestyle.png', transparent=True)


colors = ['purple','g','b']
color_dict = {eta: colors[i] for i, eta in enumerate(da_lcos.coords['C_kWh'].values)}


legendFig = gen_legend_figure(color_dict, title='$C_{kWh} [\\frac{USD}{kWh}]$', style_type='color')
legendFig.savefig('output/legend_Ckwh.png', transparent=True)


fig, axes = plt.subplots(2, sharex=True, sharey=True)

for i, coupling in enumerate(['coupled','decoupled']):

    ax=axes[i]

    da_lcos_stack = da_lcos.sel(coupling=coupling).stack(temp = ['C_kWh', 'DD_nom'])


    for C_kWh, DD_nom in da_lcos_stack.coords['temp'].values:
        da_sel = da_lcos_stack.sel(C_kWh=C_kWh, DD_nom=DD_nom)
        
        da_sel.plot(
            linestyle=linestyle_dict[DD_nom],
            linewidth=1,
            color=color_dict[C_kWh],
            ax=ax,
            label='$C_{{kWh}}$: {} USD/kWh, $\DD_{{nom}}$: {}'.format(C_kWh,DD_nom)
        )


    ax.set_title(coupling)
    plt.xscale('log')
    plt.yscale('log')
    # plt.legend(bbox_to_anchor=[0,0,1.8,1])
    plt.tight_layout()

    # plt.savefig('output/LCOS_Duration_DD_nom.png')



# %%
import xarray as xr

dec = da_lcos.sel(coupling='decoupled').isel(DD_nom=-1).drop('DD_nom').drop("coupling")
dec = dec.assign_coords(case="Decoupled: $DD_{nom} = DD$")

coup = da_lcos.sel(coupling='coupled')
cases_coup = ["Coupled: $DD_nom = {} h$".format(DD_nom.item()) for DD_nom in da_lcos.coords['DD_nom']]
cases_coup = [s.replace("DD_nom", "DD_{nom}") for s in cases_coup]
coup = coup.assign_coords(DD_nom = cases_coup).rename(DD_nom='case').drop('coupling')

da = xr.concat([dec, coup], 'case')
da


# da.plot(hue='C_kWh', linestyle='case')


#%%


linestyles = ['-','--','-.',':']
linestyle_dict = {case: linestyles[i] for i, case in enumerate(da.coords['case'].values)}


legendFig = gen_legend_figure(linestyle_dict, title=None, style_type='linestyle', figsize=(1.5,0.5))
legendFig.savefig('output/legend_linestyle.png', transparent=True)

#%%

plt.figure()

da_stack = da.stack(temp = ['C_kWh','case'])

for C_kWh, case in da_stack.coords['temp'].values:
    da_sel = da_stack.sel(C_kWh=C_kWh, case=case)
    
    da_sel.plot(
        linestyle=linestyle_dict[case],
        linewidth=1,
        color=color_dict[C_kWh],
        label='$C_{{kWh}}$: {} USD/kWh, $\DD_{{nom}}$: {}'.format(C_kWh,case)
    )

    plt.gca().set_title('')
    plt.xscale('log')
    plt.yscale('log')

plt.ylim(3e-3, 3)

plt.tight_layout()
plt.savefig('output/LCOS_DD_coupling.png')
# %%
