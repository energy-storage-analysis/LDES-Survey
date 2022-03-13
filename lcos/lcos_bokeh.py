#%%
import numpy as np

from bokeh.layouts import column, row
from bokeh.models import CustomJS, Slider
from bokeh.plotting import ColumnDataSource, figure, show, output_file
from bokeh.io import save
from sympy import O


duration = np.linspace(0, 100, 500)
lcos = [0]*len(duration)

source = ColumnDataSource(data=dict(duration=duration, lcos=lcos))

plot = figure(y_range=(0,0.2), width=400, height=400)

plot.yaxis.axis_label = "LCOS ($/kWh)"
plot.xaxis.axis_label = "Discharge Duration (h)"

plot.line('duration', 'lcos', source=source, line_width=3, line_alpha=0.6)

Ckwh_slider = Slider(start=1, end=300, value=100, step=1, title="Energy Capital Cost ($/kWh)")
Ckw_slider = Slider(start=10, end=10000, value=100, step=10, title="Power Capital Cost ($/kWh)")
eta_slider = Slider(start=0.1, end=1, value=0.8, step=.1, title="Round Trip Efficiency")
lifetime_slider = Slider(start=5, end=50, value=20, step=5, title="Lifetime (Years)")
# PE_slider = Slider(start=1, end=20, value=2.5, step=0.5, title="Price Electricity (cents/kWh)")

callback = CustomJS(args=dict(source=source, Ckwh_slider=Ckwh_slider, Ckw_slider=Ckw_slider, eta_slider=eta_slider, lifetime_slider=lifetime_slider),
                    code="""
    const data = source.data;
    const Ckwh = Ckwh_slider.value;
    const Ckw = Ckw_slider.value;
    const eta = eta_slider.value;
    const lifetime = lifetime_slider.value;
    const PE = 0.025;
    const duration = data['duration']
    const lcos = data['lcos']
    for (let i = 0; i < duration.length; i++) {
        lcos[i] = ((1/eta) - 1)*PE + (1/(lifetime*8760*eta))*(Ckw + Ckwh*duration[i]);
    }
    source.change.emit();
""")

Ckwh_slider.js_on_change('value', callback)
Ckw_slider.js_on_change('value', callback)
eta_slider.js_on_change('value', callback)
lifetime_slider.js_on_change('value', callback)
# PE_slider.js_on_change('value', callback)

# amp_slider.trigger('value', 1, 1.1)
# callback._trigger_event()

layout = row(
    plot,
    column(Ckwh_slider, Ckw_slider, eta_slider, lifetime_slider),
)


#https://stackoverflow.com/questions/58537180/how-to-access-and-update-bokeh-plots-or-widgets-using-an-external-javascript-cod
#https://github.com/bokeh/bokeh/issues/4272
# I cannot get this to work, need to move the slider manually or have redundant equation 
template = """
{% block postamble %}
    <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
    <script>
        $(document).ready(function() {
            var slider = Bokeh.documents[0].get_model_by_id("1040")
            console.log('slider value before:', slider.value)
            slider.value = 1.1
            console.log('slider value after:', slider.value)
        });
    </script>
{% endblock %}
"""

output_file('output/lcos_duration.html')

# amp_slider.value = 1.1
save(layout)

# amp_slider.value = 1.2




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
output_file('output/lcos_viability.html')
save(layout)

# amp_slider.value = 1.2