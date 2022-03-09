#%%
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams.update({'font.size' : 22})

from es import devices

#%%
fig = plt.figure(figsize=(12,8))
ax = plt.subplot(111)

for name, device in devices.items():
    print(name)
    x = device.storage_medium.energy_density.to('kWh/kg').magnitude
    y = device.transformation.power_flux.to('W/m^2').magnitude
    ax.text(y,x, name)
    ax.scatter(y, x, marker='o', color='black')

    power_name = type(device.transformation).__name__
    ax.annotate(power_name, xy=(y, 1.2), xycoords=('data', 'axes fraction'), ha='center')

    energy_name = type(device.storage_medium).__name__
    ax.annotate(energy_name, xy=(1.2, x), xycoords=('axes fraction', 'data'))


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
