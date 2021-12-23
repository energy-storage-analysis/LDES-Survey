
#%%
from bokeh.plotting import figure, show, output_notebook
from bokeh.models import HoverTool
output_notebook()

from es import read_devices
devices = read_devices()

#%%
from bokeh.models import ColumnDataSource
source = ColumnDataSource(dict(
name=[name for name in devices],
sm = [devices[name].storage_medium.name for name in devices],
pcs=[devices[name].transformation.name for name in devices],
x = [devices[name].storage_medium.energy_density for name in devices],
y = [devices[name].transformation.power_flux for name in devices]
))

p = figure(y_axis_type='log', x_axis_type='log')
p.add_tools(HoverTool(tooltips=[
    ('name', '@name'),
   ('sm', '@sm'),
   ('pcs', '@pcs')
   ]))
p.circle(source=source, x='x',y='y', size=20)

show(p)
