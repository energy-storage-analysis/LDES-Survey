
#%%
from bokeh.plotting import figure, show, output_notebook
from bokeh.models import HoverTool
output_notebook()

from es import devices


#%%
from bokeh.models import ColumnDataSource
source = ColumnDataSource(dict(
name=[name for name in devices],
sm = [type(devices[name].storage_medium).__name__ for name in devices],
pcs=[type(devices[name].transformation).__name__ for name in devices],
y = [devices[name].storage_medium.energy_density.to('kWh/kg').magnitude for name in devices],
x = [devices[name].transformation.power_flux.to('W/m^2').magnitude for name in devices]
))

p = figure(y_axis_type='log', x_axis_type='log')
p.add_tools(HoverTool(tooltips=[
    ('name', '@name'),
   ('sm', '@sm'),
   ('pcs', '@pcs')
   ]))
p.circle(source=source, x='x',y='y', size=20)

show(p)

# %%
