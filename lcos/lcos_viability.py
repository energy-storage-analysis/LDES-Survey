#%%
import numpy as np

from bokeh.layouts import column, row
from bokeh.models import CustomJS, Slider
from bokeh.plotting import ColumnDataSource, figure, show
from bokeh.io import save

C_kWh = np.logspace(0, 3, 500)
C_kW = [0]*len(C_kWh)

source = ColumnDataSource(data=dict(C_kWh=C_kWh, C_kW=C_kW))

plot = figure(y_range = (1e1, 1e5), width=400, height=400, y_axis_type='log', x_axis_type='log')

plot.yaxis.axis_label = "Power Capital Cost ($/kWh)"
plot.xaxis.axis_label = "Energy Capital Cost ($/kWh)"

plot.line('C_kWh', 'C_kW', source=source, line_width=3, line_alpha=0.6)

eta_slider = Slider(start=0.5, end=1, value=0.8, step=.1, title="Round Trip Efficiency")
lifetime_slider = Slider(start=5, end=50, value=20, step=5, title="Lifetime (y)")
duration_slider = Slider(start=1, end=300, value=100, step=1, title="Discharge Duration (h)")
PE_slider = Slider(start=1, end=20, value=2.5, step=0.5, title="Price Electricity (cents/kWh)")
LCOS_slider = Slider(start=1, end=20, value=5, step=0.5, title="Target LCOS (cents/kWh)")

callback = CustomJS(args=dict(source=source, duration_slider=duration_slider, eta_slider=eta_slider, lifetime_slider=lifetime_slider, PE_slider=PE_slider, LCOS_slider=LCOS_slider),
                    code="""
    const data = source.data;
    const duration = duration_slider.value;
    const eta = eta_slider.value;
    const lifetime = lifetime_slider.value;
    const LCOS = LCOS_slider.value/100;
    const PE = PE_slider.value/100;
    const C_kW = data['C_kW']
    const C_kWh = data['C_kWh']
    for (let i = 0; i < C_kWh.length; i++) {
        C_kW[i] = lifetime*8760*eta*( LCOS - ( (1/eta)-1 )*PE ) - C_kWh[i]*duration;
    }
    source.change.emit();
""")

duration_slider.js_on_change('value', callback)
eta_slider.js_on_change('value', callback)
lifetime_slider.js_on_change('value', callback)
PE_slider.js_on_change('value', callback)
LCOS_slider.js_on_change('value', callback)

# amp_slider.trigger('value', 1, 1.1)
# callback._trigger_event()

layout = row(
    plot,
    column(LCOS_slider, PE_slider, duration_slider,  eta_slider, lifetime_slider),
)



# amp_slider.value = 1.1
save(layout)

# amp_slider.value = 1.2