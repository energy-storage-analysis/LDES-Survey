
#%%
from bokeh.plotting import figure, show, output_notebook
from bokeh.models import HoverTool, LabelSet
output_notebook()

from es import devices


#%%
from bokeh.models import ColumnDataSource
source = ColumnDataSource(dict(
name=[name for name in devices],
long_name=[devices[name].name for name in devices],
sm = [str(devices[name].storage_medium) for name in devices],
pcs=[str(devices[name].transformation) for name in devices],
y = [devices[name].storage_medium.energy_density.to('kWh/kg').magnitude for name in devices],
x = [devices[name].transformation.power_flux.to('W/m^2').magnitude for name in devices]
))

p = figure(y_axis_type='log', x_axis_type='log')
p.add_tools(HoverTool(tooltips=[
    ('name', '@long_name'),
   ('Storage Medium', '@sm'),
   ('Power Conversion System', '@pcs')
   ]))
p.circle(source=source, x='x',y='y', size=50)


labels = LabelSet(x='x', y='y', text='name', text_align='center', text_color='black',
              x_offset=0, y_offset=0, source=source, render_mode='canvas')

p.add_layout(labels)

show(p)

# %%
