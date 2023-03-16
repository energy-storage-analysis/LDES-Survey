#%%
import numpy as np

from bokeh.layouts import column, row
from bokeh.models import CustomJS, Slider, Div
from bokeh.plotting import ColumnDataSource, figure, show, output_file
from bokeh.io import save, curdoc
import os

if not os.path.exists('output_bokeh'): os.mkdir('output_bokeh')

### Duration dependence

duration = np.linspace(0, 100, 500)
lcos = [0]*len(duration)

source = ColumnDataSource(data=dict(duration=duration, lcos=lcos))

plot = figure(y_range=(0,0.2), width=800, height=400)

plot.yaxis.axis_label = "LCOS (USD/kWh)"
plot.yaxis.major_label_text_font_size = "12pt"
plot.yaxis.axis_label_text_font_size = "12pt"

plot.xaxis.axis_label = "Discharge Duration (hours)"
plot.xaxis.major_label_text_font_size = "12pt"
plot.xaxis.axis_label_text_font_size = "12pt"

plot.line('duration', 'lcos', source=source, line_width=3, line_alpha=0.6)

Ckwh_slider = Slider(start=1, end=300, value=100, step=1, title=r"$$C_{kWh} (USD/kWh)$$")
Ckw_slider = Slider(start=100, end=2000, value=1000, step=10, title="$$C_{kW} (USD/kW)$$")
eta_slider = Slider(start=0.1, end=1, value=0.8, step=.01, title="$$\eta_{RT}$$")
lifetime_slider = Slider(start=5, end=50, value=20, step=1, title="Lifetime (Years)")
discount_slider = Slider(start=0.01, end=.2, value=0.05, step=.01, title="Discount Rate")
PE_slider = Slider(start=0.01, end=0.1, value=0.05, step=0.01, title="$$P_{chg} (USD/kWh)$$")

p_text = Div(text="""<p style="font-size:16pt;">This is a paragraph.</p>""",
width=200, height=100)




callback = CustomJS(args=dict(source=source, 
                              Ckwh_slider=Ckwh_slider, 
                              Ckw_slider=Ckw_slider, 
                              eta_slider=eta_slider, 
                              lifetime_slider=lifetime_slider,
                              discount_slider=discount_slider,
                              PE_slider=PE_slider,
                              p_text=p_text
                              ),
                    code="""
    const data = source.data;
    const Ckwh = Ckwh_slider.value;
    const Ckw = Ckw_slider.value;
    const eta = eta_slider.value;
    const LT = lifetime_slider.value;
    const r = discount_slider.value;
    const PE = PE_slider.value;

    const LT_eff = (1 - 1/(1 + r)**LT)/r;


    const duration = data['duration']
    const lcos = data['lcos']
    for (let i = 0; i < duration.length; i++) {
        lcos[i] = ((1/eta) - 1)*PE + (1/(LT_eff*8760*eta))*(Ckw + Ckwh*duration[i]);
    }

    p_text.text = "<p style=font-size:16pt;>LCOS at 100 hours: ".concat(lcos[duration.length - 1].toFixed(3), " USD/kWh <\p>")
    source.change.emit();
""")

Ckwh_slider.js_on_change('value', callback)
Ckw_slider.js_on_change('value', callback)
eta_slider.js_on_change('value', callback)
lifetime_slider.js_on_change('value', callback)
discount_slider.js_on_change('value', callback)
PE_slider.js_on_change('value', callback)

layout = row(
    plot,
    column(Ckwh_slider, Ckw_slider, eta_slider, lifetime_slider, discount_slider, PE_slider, p_text),
)

# This is so the line will show up upon document load. 
# https://github.com/bokeh/bokeh/pull/12370

curdoc().js_on_event("document_ready", callback)

output_file('output_bokeh/lcos_duration.html')
save(layout)


### Maximum power capital 

C_kWh = np.logspace(0, 3, 500)
C_kW = [0]*len(C_kWh)

source = ColumnDataSource(data=dict(C_kWh=C_kWh, C_kW=C_kW))

plot = figure(y_range = (1e1, 1e5), width=1000, height=500, y_axis_type='log', x_axis_type='log')

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

layout = row(
    plot,
    column(LCOS_slider, PE_slider, duration_slider,  eta_slider, lifetime_slider),
)


curdoc().js_on_event("document_ready", callback)

output_file('output_bokeh/lcos_viability.html')
save(layout)
