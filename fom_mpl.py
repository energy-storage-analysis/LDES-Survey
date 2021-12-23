#%%
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams.update({'font.size' : 22})

from es import read_devices
devices = read_devices()
#%%
fig = plt.figure(figsize=(12,8))
ax = plt.subplot(111)

for name, device in devices.items():
    x = device.storage_medium.energy_density
    y = device.transformation.power_flux
    ax.text(y,x, name)
    ax.scatter(y, x, marker='o', color='black')

sms = set([devices[name].storage_medium for name in devices])
tds = set([devices[name].transformation for name in devices])

for td in tds:
    power_density = td.power_flux
    ax.annotate(td.name, xy=(power_density, 1.2), xycoords=('data', 'axes fraction'), ha='center')

for sm in sms:
    energy_density = sm.energy_density
    ax.annotate(sm.name, xy=(1.2, energy_density), xycoords=('axes fraction', 'data'))
    # plt.axhline(energy_density, xmax=1.2)

from matplotlib.patches import Rectangle
# rect = Rectangle(xy=(power_density, energy_density), width = 100000, height = 1000)
# ax.add_patch(rect)

ax.set_xscale('log')
ax.set_yscale('log')

# ax.set_ylim(1e-3,40)
# ax.set_xlim(0.01,1e12)

# ax.yaxis.tick_right()
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')

ax.grid()
ax.set_xlabel('Power Flux $(W/m^2)$')
ax.set_ylabel('Energy Density $(kWh/kg)$')
# %%
