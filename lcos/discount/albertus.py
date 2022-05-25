#%%
import matplotlib.pyplot as plt
import numpy as np
import numpy_financial as npf
import seaborn as sns
import xyzpy
# %%

def calc_PVR(nc, d, deltaE, Rp, r, lifetime):
    term = deltaE*nc + Rp/d
    return npf.npv(r , [term]*lifetime)

def calc_OP(nc, d, eta_RT, Pc, VOM, FOM, r, lifetime):
    term = nc*Pc*((1/eta_RT)-1) + nc*VOM + FOM/d
    return npf.npv(r, [term]*lifetime)

def calc_capital(Cp, Ce, d, eta_RT):
    eta_d = np.sqrt(eta_RT)
    return Cp/d + Ce/eta_d

@xyzpy.label(var_names=['cap_cost'])
def infer_capital(nc, d, deltaE, Rp, eta_RT, Pc, VOM, FOM, r, lifetime):
    PVR = calc_PVR(nc, d, deltaE, Rp, r, lifetime)
    OP = calc_OP(nc, d,eta_RT, Pc, VOM, FOM, r, lifetime)
    cap = PVR - OP 
    return cap if cap > 0 else np.nan

combos = dict(
d = [10,50,100],
eta_RT = np.linspace(0, 1, 50),
nc = np.linspace(0, 100, 50)
)

FOM_pct = 0.01 
# C_re = 0 #Not specified...

constants =dict(
lifetime = 20,
r = 0.10,
Rp = 25,
VOM = 0.002,
FOM = 10*FOM_pct, #Guess...
deltaE = 0.05,
Pc = 0.025,
)

da_cap = infer_capital.run_combos(combos, constants=constants)['cap_cost']

#%%
levels = [0,10,20,30]

g = da_cap.plot(col='d')

for i, ax in enumerate(g.axes.flatten()):
    d = combos['d'][i]
    da_cap.sel(d=d).plot.contour(ax=ax, colors='black', levels=levels)

# plt.legend()

#%%



